-- ETL Procedures for BACEN Data Migration
-- Optimized for transforming existing CSV/JSON data into the new schema

-- =============================================
-- ETL HELPER FUNCTIONS
-- =============================================

-- Function to safely convert text to numeric
CREATE OR REPLACE FUNCTION safe_numeric(input_text TEXT)
RETURNS NUMERIC AS $$
BEGIN
    IF input_text IS NULL OR input_text = '' OR input_text = 'null' THEN
        RETURN NULL;
    END IF;
    
    -- Clean the input: remove currency symbols, commas, etc.
    input_text := REPLACE(input_text, 'R$', '');
    input_text := REPLACE(input_text, ',', '');
    input_text := REPLACE(input_text, ' ', '');
    
    RETURN input_text::NUMERIC;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Function to extract quarter from period string
CREATE OR REPLACE FUNCTION extract_quarter_info(periodo TEXT)
RETURNS TABLE(year_val INTEGER, quarter_val INTEGER, quarter_text_val TEXT) AS $$
BEGIN
    -- Handle formats like "2024T4", "2024-T4", "T4-2024", etc.
    IF periodo ~ '^\d{4}T[1-4]$' THEN
        year_val := LEFT(periodo, 4)::INTEGER;
        quarter_val := RIGHT(periodo, 1)::INTEGER;
        quarter_text_val := 'T' || quarter_val::TEXT;
        RETURN NEXT;
    ELSIF periodo ~ '^\d{4}-T[1-4]$' THEN
        year_val := LEFT(periodo, 4)::INTEGER;
        quarter_val := RIGHT(periodo, 1)::INTEGER;
        quarter_text_val := 'T' || quarter_val::TEXT;
        RETURN NEXT;
    ELSIF periodo ~ '^T[1-4]-\d{4}$' THEN
        quarter_val := SUBSTRING(periodo, 2, 1)::INTEGER;
        year_val := RIGHT(periodo, 4)::INTEGER;
        quarter_text_val := 'T' || quarter_val::TEXT;
        RETURN NEXT;
    ELSE
        -- Default to current year Q4 if parsing fails
        year_val := 2024;
        quarter_val := 4;
        quarter_text_val := 'T4';
        RETURN NEXT;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- STAGING TABLES FOR ETL
-- =============================================

-- Staging table that matches the current BACEN CSV structure
CREATE TABLE IF NOT EXISTS staging_bacen_raw (
    id SERIAL PRIMARY KEY,
    tipo_instituicao TEXT,
    cod_inst TEXT,
    nome_instituicao TEXT,
    segmento TEXT,
    periodo TEXT,
    nome_relatorio TEXT,
    grupo TEXT,
    nome_coluna TEXT,
    valor TEXT, -- Keep as text initially for cleaning
    
    -- ETL tracking
    processed BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- MAIN ETL PROCEDURE
-- =============================================

CREATE OR REPLACE FUNCTION process_bacen_data_batch(batch_size INTEGER DEFAULT 1000)
RETURNS TABLE(processed_count INTEGER, error_count INTEGER, status TEXT) AS $$
DECLARE
    rec RECORD;
    institution_uuid UUID;
    time_period_uuid UUID;
    report_type_uuid UUID;
    metric_group_uuid UUID;
    metric_uuid UUID;
    clean_valor NUMERIC;
    quarter_info RECORD;
    processed_records INTEGER := 0;
    error_records INTEGER := 0;
    total_batch INTEGER;
BEGIN
    -- Get batch of unprocessed records
    SELECT COUNT(*) INTO total_batch 
    FROM staging_bacen_raw 
    WHERE processed = FALSE 
    LIMIT batch_size;
    
    IF total_batch = 0 THEN
        processed_count := 0;
        error_count := 0;
        status := 'NO_DATA_TO_PROCESS';
        RETURN NEXT;
        RETURN;
    END IF;
    
    -- Process each record in the batch
    FOR rec IN 
        SELECT * FROM staging_bacen_raw 
        WHERE processed = FALSE 
        ORDER BY id 
        LIMIT batch_size
    LOOP
        BEGIN
            -- Extract quarter information
            SELECT * INTO quarter_info 
            FROM extract_quarter_info(rec.periodo);
            
            -- Get or create time period
            SELECT id INTO time_period_uuid
            FROM time_periods
            WHERE year = quarter_info.year_val AND quarter = quarter_info.quarter_val;
            
            IF time_period_uuid IS NULL THEN
                INSERT INTO time_periods (year, quarter, quarter_text, start_date, end_date)
                VALUES (
                    quarter_info.year_val,
                    quarter_info.quarter_val,
                    quarter_info.quarter_text_val,
                    (quarter_info.year_val || '-' || LPAD(((quarter_info.quarter_val-1)*3+1)::TEXT, 2, '0') || '-01')::DATE,
                    (quarter_info.year_val || '-' || LPAD((quarter_info.quarter_val*3)::TEXT, 2, '0') || '-' || 
                     CASE quarter_info.quarter_val 
                        WHEN 1 THEN '31'
                        WHEN 2 THEN '30' 
                        WHEN 3 THEN '30'
                        WHEN 4 THEN '31'
                     END)::DATE
                )
                RETURNING id INTO time_period_uuid;
            END IF;
            
            -- Get or create institution
            SELECT id INTO institution_uuid
            FROM institutions
            WHERE cod_inst = rec.cod_inst;
            
            IF institution_uuid IS NULL THEN
                INSERT INTO institutions (cod_inst, cnpj, name, short_name, type, segment, control_type, region, city)
                VALUES (
                    rec.cod_inst,
                    COALESCE(rec.cod_inst, 'UNKNOWN') || '/0001-00', -- Generate fake CNPJ if missing
                    rec.nome_instituicao,
                    CASE 
                        WHEN LENGTH(rec.nome_instituicao) > 50 
                        THEN LEFT(rec.nome_instituicao, 47) || '...'
                        ELSE rec.nome_instituicao
                    END,
                    'Banco', -- Default type
                    COALESCE(rec.segmento, 'S5'),
                    'Desconhecido',
                    'BR', -- Default region
                    'Não Informado'
                )
                RETURNING id INTO institution_uuid;
            END IF;
            
            -- Get or create report type
            SELECT id INTO report_type_uuid
            FROM report_types
            WHERE nome_relatorio = rec.nome_relatorio;
            
            IF report_type_uuid IS NULL THEN
                INSERT INTO report_types (nome_relatorio, categoria, description)
                VALUES (
                    rec.nome_relatorio,
                    'Other', -- Default category
                    'Auto-imported from BACEN data'
                )
                RETURNING id INTO report_type_uuid;
            END IF;
            
            -- Get or create metric group
            SELECT id INTO metric_group_uuid
            FROM metric_groups
            WHERE grupo = rec.grupo;
            
            IF metric_group_uuid IS NULL THEN
                INSERT INTO metric_groups (grupo, categoria, description)
                VALUES (
                    rec.grupo,
                    'Auto_Import',
                    'Auto-imported from BACEN data'
                )
                RETURNING id INTO metric_group_uuid;
            END IF;
            
            -- Get or create metric
            SELECT id INTO metric_uuid
            FROM metrics
            WHERE nome_coluna = rec.nome_coluna;
            
            IF metric_uuid IS NULL THEN
                INSERT INTO metrics (nome_coluna, tipo_dado, unidade, description)
                VALUES (
                    rec.nome_coluna,
                    CASE 
                        WHEN rec.nome_coluna ~* '(quantidade|número|total de|qtd)' THEN 'count'
                        WHEN rec.nome_coluna ~* '(índice|ratio|%|percentual|taxa)' THEN 'ratio'
                        ELSE 'currency'
                    END,
                    CASE 
                        WHEN rec.nome_coluna ~* '(quantidade|número|total de|qtd)' THEN 'quantidade'
                        WHEN rec.nome_coluna ~* '(índice|ratio|%|percentual|taxa)' THEN '%'
                        ELSE 'R$ milhões'
                    END,
                    'Auto-imported from BACEN data'
                )
                RETURNING id INTO metric_uuid;
            END IF;
            
            -- Clean and convert the value
            clean_valor := safe_numeric(rec.valor);
            
            -- Insert into financial_data (with upsert to handle duplicates)
            INSERT INTO financial_data (
                institution_id,
                time_period_id,
                report_type_id,
                metric_group_id,
                metric_id,
                valor,
                data_source
            ) VALUES (
                institution_uuid,
                time_period_uuid,
                report_type_uuid,
                metric_group_uuid,
                metric_uuid,
                clean_valor,
                'BACEN_ETL_IMPORT'
            )
            ON CONFLICT (institution_id, time_period_id, report_type_id, metric_group_id, metric_id, 
                        geographic_region_id, risk_level, maturity_bucket, indexer)
            DO UPDATE SET 
                valor = EXCLUDED.valor,
                updated_at = NOW();
            
            -- Mark as processed
            UPDATE staging_bacen_raw 
            SET processed = TRUE, error_message = NULL
            WHERE id = rec.id;
            
            processed_records := processed_records + 1;
            
        EXCEPTION WHEN OTHERS THEN
            -- Log the error and mark as processed to avoid infinite loops
            UPDATE staging_bacen_raw 
            SET processed = TRUE, error_message = SQLERRM
            WHERE id = rec.id;
            
            error_records := error_records + 1;
            
            -- Continue processing other records
        END;
    END LOOP;
    
    processed_count := processed_records;
    error_count := error_records;
    status := 'COMPLETED_BATCH';
    RETURN NEXT;
    
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- CONVENIENCE PROCEDURES
-- =============================================

-- Process all pending data
CREATE OR REPLACE FUNCTION process_all_bacen_data()
RETURNS TABLE(total_processed INTEGER, total_errors INTEGER, status TEXT) AS $$
DECLARE
    batch_result RECORD;
    total_proc INTEGER := 0;
    total_err INTEGER := 0;
    remaining INTEGER;
BEGIN
    LOOP
        -- Process a batch
        SELECT * INTO batch_result FROM process_bacen_data_batch(1000);
        
        total_proc := total_proc + batch_result.processed_count;
        total_err := total_err + batch_result.error_count;
        
        -- Check if there are more records to process
        SELECT COUNT(*) INTO remaining FROM staging_bacen_raw WHERE processed = FALSE;
        
        EXIT WHEN remaining = 0;
        
        -- Small delay to prevent overwhelming the system
        PERFORM pg_sleep(0.1);
    END LOOP;
    
    total_processed := total_proc;
    total_errors := total_err;
    status := 'ALL_DATA_PROCESSED';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Clear staging table
CREATE OR REPLACE FUNCTION clear_staging_data()
RETURNS VOID AS $$
BEGIN
    TRUNCATE staging_bacen_raw RESTART IDENTITY;
END;
$$ LANGUAGE plpgsql;

-- Get processing status
CREATE OR REPLACE FUNCTION get_etl_status()
RETURNS TABLE(
    total_staging_records INTEGER,
    processed_records INTEGER,
    error_records INTEGER,
    pending_records INTEGER,
    processing_percentage NUMERIC
) AS $$
BEGIN
    SELECT 
        COUNT(*),
        COUNT(*) FILTER (WHERE processed = TRUE AND error_message IS NULL),
        COUNT(*) FILTER (WHERE processed = TRUE AND error_message IS NOT NULL),
        COUNT(*) FILTER (WHERE processed = FALSE)
    INTO total_staging_records, processed_records, error_records, pending_records
    FROM staging_bacen_raw;
    
    processing_percentage := CASE 
        WHEN total_staging_records = 0 THEN 0
        ELSE ROUND((processed_records::NUMERIC / total_staging_records::NUMERIC) * 100, 2)
    END;
    
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- SAMPLE DATA LOADER
-- =============================================
-- Load sample data based on frontend mockData for testing

CREATE OR REPLACE FUNCTION load_sample_data()
RETURNS VOID AS $$
DECLARE
    bb_uuid UUID;
    itau_uuid UUID;
    time_2024t4_uuid UUID;
    ativo_report_uuid UUID;
    demonstracao_report_uuid UUID;
    nagroup_uuid UUID;
    ativo_total_uuid UUID;
    lucro_liquido_uuid UUID;
BEGIN
    -- Get UUIDs for sample data
    SELECT id INTO bb_uuid FROM institutions WHERE cod_inst = 'C0000001';
    SELECT id INTO itau_uuid FROM institutions WHERE cod_inst = 'C0000341';
    SELECT id INTO time_2024t4_uuid FROM time_periods WHERE year = 2024 AND quarter = 4;
    SELECT id INTO ativo_report_uuid FROM report_types WHERE nome_relatorio = 'Ativo';
    SELECT id INTO demonstracao_report_uuid FROM report_types WHERE nome_relatorio = 'Demonstração de Resultado';
    SELECT id INTO nagroup_uuid FROM metric_groups WHERE grupo = 'nagroup';
    SELECT id INTO ativo_total_uuid FROM metrics WHERE nome_coluna = 'Ativo Total';
    SELECT id INTO lucro_liquido_uuid FROM metrics WHERE nome_coluna = 'Lucro Líquido';
    
    -- Insert sample financial data
    INSERT INTO financial_data (
        institution_id, time_period_id, report_type_id, 
        metric_group_id, metric_id, valor, data_source
    ) VALUES
    -- Banco do Brasil sample data
    (bb_uuid, time_2024t4_uuid, ativo_report_uuid, nagroup_uuid, ativo_total_uuid, 2100000.00, 'SAMPLE_DATA'),
    (bb_uuid, time_2024t4_uuid, demonstracao_report_uuid, nagroup_uuid, lucro_liquido_uuid, 38200.00, 'SAMPLE_DATA'),
    
    -- Itaú sample data  
    (itau_uuid, time_2024t4_uuid, ativo_report_uuid, nagroup_uuid, ativo_total_uuid, 1900000.00, 'SAMPLE_DATA'),
    (itau_uuid, time_2024t4_uuid, demonstracao_report_uuid, nagroup_uuid, lucro_liquido_uuid, 42100.00, 'SAMPLE_DATA')
    
    ON CONFLICT DO NOTHING;
    
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- REFRESH VIEWS PROCEDURE
-- =============================================

CREATE OR REPLACE FUNCTION refresh_materialized_views_with_log()
RETURNS TABLE(view_name TEXT, refresh_time INTERVAL, status TEXT) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    -- Market Share View
    start_time := clock_timestamp();
    REFRESH MATERIALIZED VIEW market_share_view;
    end_time := clock_timestamp();
    
    view_name := 'market_share_view';
    refresh_time := end_time - start_time;
    status := 'SUCCESS';
    RETURN NEXT;
    
    -- Institution Summary View
    start_time := clock_timestamp();
    REFRESH MATERIALIZED VIEW institution_summary_view;
    end_time := clock_timestamp();
    
    view_name := 'institution_summary_view';
    refresh_time := end_time - start_time;
    status := 'SUCCESS';
    RETURN NEXT;
    
    -- Credit Portfolio View
    start_time := clock_timestamp();
    REFRESH MATERIALIZED VIEW credit_portfolio_view;
    end_time := clock_timestamp();
    
    view_name := 'credit_portfolio_view';
    refresh_time := end_time - start_time;
    status := 'SUCCESS';
    RETURN NEXT;
    
END;
$$ LANGUAGE plpgsql;