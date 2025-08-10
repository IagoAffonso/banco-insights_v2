-- Banco Insights 2.0 Database Schema
-- Optimized for Supabase PostgreSQL with performance and frontend requirements

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- =============================================
-- DIMENSION TABLES
-- =============================================

-- Institution Master Table
-- Based on frontend mockData Institution interface and BACEN IFDATA structure
CREATE TABLE institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cod_inst VARCHAR(20) NOT NULL UNIQUE, -- BACEN institution code
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'Banco Múltiplo', 'Banco Digital', etc.
    segment VARCHAR(2) NOT NULL, -- S1, S2, S3, S4, S5
    control_type TEXT NOT NULL, -- 'Público', 'Privado Nacional', 'Privado Estrangeiro'
    region VARCHAR(2) NOT NULL, -- Brazilian state codes
    city TEXT NOT NULL,
    founded_year INTEGER,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes for performance
    CONSTRAINT valid_segment CHECK (segment IN ('S1', 'S2', 'S3', 'S4', 'S5'))
);

-- Report Types Dimension
-- Based on EDA analysis: 13 report types identified
CREATE TABLE report_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome_relatorio TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL, -- 'Financial', 'Credit', 'Risk', 'Capital'
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Metric Groups Dimension  
-- Based on EDA analysis: 54 unique groups identified
CREATE TABLE metric_groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    grupo TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL, -- Credit products, Economic sectors, etc.
    parent_group_id UUID REFERENCES metric_groups(id),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Metrics Dimension
-- Based on EDA analysis: 208 unique columns/metrics identified
CREATE TABLE metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome_coluna TEXT NOT NULL UNIQUE,
    tipo_dado TEXT NOT NULL, -- 'currency', 'percentage', 'count', 'ratio'
    unidade TEXT, -- 'R$ milhões', '%', 'quantity'
    description TEXT,
    calculation_formula TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Time Periods Dimension
-- Optimized for quarterly Brazilian financial reporting
CREATE TABLE time_periods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    quarter_text VARCHAR(2) NOT NULL, -- 'T1', 'T2', 'T3', 'T4'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(year, quarter)
);

-- Geographic Regions Dimension
-- Based on EDA analysis: Brazilian regions + international
CREATE TABLE geographic_regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'state', 'region', 'international'
    parent_region_id UUID REFERENCES geographic_regions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- FACT TABLES
-- =============================================

-- Main Financial Data Fact Table
-- Optimized for high-performance queries and frontend needs
CREATE TABLE financial_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID NOT NULL REFERENCES institutions(id),
    time_period_id UUID NOT NULL REFERENCES time_periods(id),
    report_type_id UUID NOT NULL REFERENCES report_types(id),
    metric_group_id UUID NOT NULL REFERENCES metric_groups(id),
    metric_id UUID NOT NULL REFERENCES metrics(id),
    
    -- Value with proper numeric precision for financial data
    valor NUMERIC(20, 2) NOT NULL,
    
    -- Additional context fields
    geographic_region_id UUID REFERENCES geographic_regions(id),
    risk_level VARCHAR(2), -- AA, A, B, C, D, E, F, G, H for credit risk
    maturity_bucket TEXT, -- Maturity classifications from EDA
    indexer TEXT, -- Interest rate indexers: Prefixado, CDI, SELIC, etc.
    
    -- Audit fields
    data_source TEXT DEFAULT 'BACEN_IFDATA',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Composite unique constraint to prevent duplicates
    UNIQUE(institution_id, time_period_id, report_type_id, metric_group_id, metric_id, geographic_region_id, risk_level, maturity_bucket, indexer)
);

-- =============================================
-- MATERIALIZED VIEWS FOR PERFORMANCE
-- =============================================

-- Market Share Aggregated View
-- Pre-calculated for dashboard performance
CREATE MATERIALIZED VIEW market_share_view AS
SELECT 
    fd.institution_id,
    i.name as institution_name,
    i.short_name,
    i.segment,
    tp.year,
    tp.quarter,
    tp.quarter_text,
    rt.nome_relatorio as report_type,
    m.nome_coluna as metric_name,
    
    -- Market share calculation
    fd.valor as institution_value,
    SUM(fd.valor) OVER (PARTITION BY tp.id, rt.id, m.id) as market_total,
    ROUND(
        (fd.valor / NULLIF(SUM(fd.valor) OVER (PARTITION BY tp.id, rt.id, m.id), 0)) * 100, 
        2
    ) as market_share_pct,
    
    -- Ranking
    ROW_NUMBER() OVER (
        PARTITION BY tp.id, rt.id, m.id 
        ORDER BY fd.valor DESC
    ) as market_rank
    
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN time_periods tp ON fd.time_period_id = tp.id
JOIN report_types rt ON fd.report_type_id = rt.id
JOIN metrics m ON fd.metric_id = m.id
WHERE i.status = 'active';

-- Institution Summary View
-- Optimized for institution detail pages
CREATE MATERIALIZED VIEW institution_summary_view AS
SELECT 
    i.id as institution_id,
    i.cod_inst,
    i.name,
    i.short_name,
    i.segment,
    i.control_type,
    tp.year,
    tp.quarter_text,
    
    -- Key Financial Metrics (based on frontend mockData structure)
    MAX(CASE WHEN m.nome_coluna = 'Ativo Total' THEN fd.valor END) as total_assets,
    MAX(CASE WHEN m.nome_coluna = 'Operações de Crédito' THEN fd.valor END) as credit_operations,
    MAX(CASE WHEN m.nome_coluna = 'TVM e Instrumentos Financeiros Derivativos' THEN fd.valor END) as securities,
    MAX(CASE WHEN m.nome_coluna = 'Disponibilidades' THEN fd.valor END) as cash,
    MAX(CASE WHEN m.nome_coluna = 'Total da Carteira de Pessoa Física' THEN fd.valor END) as retail_credit,
    MAX(CASE WHEN m.nome_coluna = 'Total da Carteira de Pessoa Jurídica' THEN fd.valor END) as corporate_credit,
    MAX(CASE WHEN m.nome_coluna = 'Lucro Líquido' THEN fd.valor END) as net_income,
    MAX(CASE WHEN m.nome_coluna = 'Patrimônio de Referência' THEN fd.valor END) as regulatory_capital,
    MAX(CASE WHEN m.nome_coluna = 'Índice de Basileia' THEN fd.valor END) as basel_ratio
    
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN time_periods tp ON fd.time_period_id = tp.id
JOIN metrics m ON fd.metric_id = m.id
WHERE i.status = 'active'
GROUP BY i.id, i.cod_inst, i.name, i.short_name, i.segment, i.control_type, tp.year, tp.quarter_text, tp.id
ORDER BY i.name, tp.year DESC, tp.quarter DESC;

-- Credit Portfolio Detailed View
-- Optimized for credit analysis features
CREATE MATERIALIZED VIEW credit_portfolio_view AS
SELECT 
    fd.institution_id,
    i.name as institution_name,
    tp.year,
    tp.quarter_text,
    mg.grupo as product_group,
    gr.name as geographic_region,
    fd.risk_level,
    fd.maturity_bucket,
    fd.indexer,
    m.nome_coluna as metric_name,
    fd.valor as portfolio_value,
    
    -- Percentage within institution
    ROUND(
        (fd.valor / NULLIF(
            SUM(fd.valor) OVER (
                PARTITION BY fd.institution_id, tp.id 
                WHERE rt.categoria = 'Credit'
            ), 0
        )) * 100, 2
    ) as institution_share_pct
    
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN time_periods tp ON fd.time_period_id = tp.id
JOIN report_types rt ON fd.report_type_id = rt.id
JOIN metric_groups mg ON fd.metric_group_id = mg.id
JOIN metrics m ON fd.metric_id = m.id
LEFT JOIN geographic_regions gr ON fd.geographic_region_id = gr.id
WHERE rt.categoria = 'Credit' AND i.status = 'active';

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Core indexes for fact table queries
CREATE INDEX idx_financial_data_institution_time ON financial_data(institution_id, time_period_id);
CREATE INDEX idx_financial_data_report_metric ON financial_data(report_type_id, metric_id);
CREATE INDEX idx_financial_data_composite_query ON financial_data(institution_id, time_period_id, report_type_id);
CREATE INDEX idx_financial_data_valor ON financial_data(valor) WHERE valor IS NOT NULL;

-- Time-based indexes for time series queries
CREATE INDEX idx_time_periods_year_quarter ON time_periods(year DESC, quarter DESC);
CREATE INDEX idx_financial_data_time_lookup ON financial_data(time_period_id) INCLUDE (institution_id, valor);

-- Institution lookup indexes
CREATE INDEX idx_institutions_segment ON institutions(segment) WHERE status = 'active';
CREATE INDEX idx_institutions_type ON institutions(type) WHERE status = 'active';
CREATE INDEX idx_institutions_search ON institutions USING gin(name gin_trgm_ops);

-- Metric and group search indexes  
CREATE INDEX idx_metrics_search ON metrics USING gin(nome_coluna gin_trgm_ops);
CREATE INDEX idx_metric_groups_categoria ON metric_groups(categoria);

-- Geographic and risk indexes
CREATE INDEX idx_financial_data_geographic ON financial_data(geographic_region_id) WHERE geographic_region_id IS NOT NULL;
CREATE INDEX idx_financial_data_risk ON financial_data(risk_level) WHERE risk_level IS NOT NULL;

-- =============================================
-- FUNCTIONS AND TRIGGERS
-- =============================================

-- Auto-update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers
CREATE TRIGGER update_institutions_updated_at BEFORE UPDATE ON institutions 
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
    
CREATE TRIGGER update_financial_data_updated_at BEFORE UPDATE ON financial_data 
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW market_share_view;
    REFRESH MATERIALIZED VIEW institution_summary_view; 
    REFRESH MATERIALIZED VIEW credit_portfolio_view;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- ROW LEVEL SECURITY (RLS) FOR SUPABASE
-- =============================================

-- Enable RLS on sensitive tables
ALTER TABLE institutions ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_data ENABLE ROW LEVEL SECURITY;

-- Basic read policy for authenticated users
CREATE POLICY "Allow read access to authenticated users" ON institutions
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Allow read access to financial data" ON financial_data
    FOR SELECT TO authenticated USING (true);

-- Admin write policies (to be customized based on user roles)
CREATE POLICY "Allow admin write access" ON institutions
    FOR ALL TO authenticated 
    USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Allow admin write access to financial data" ON financial_data
    FOR ALL TO authenticated
    USING (auth.jwt() ->> 'role' = 'admin');

-- =============================================
-- INITIAL DATA SETUP
-- =============================================

-- Insert Brazilian geographic regions
INSERT INTO geographic_regions (code, name, type) VALUES
('BR', 'Brasil', 'country'),
('N', 'Norte', 'region'),
('NE', 'Nordeste', 'region'), 
('CO', 'Centro-Oeste', 'region'),
('SE', 'Sudeste', 'region'),
('S', 'Sul', 'region'),
('EXT', 'Exterior', 'international');

-- Insert common time periods for Brazilian financial reporting
INSERT INTO time_periods (year, quarter, quarter_text, start_date, end_date, is_current) VALUES
(2020, 1, 'T1', '2020-01-01', '2020-03-31', false),
(2020, 2, 'T2', '2020-04-01', '2020-06-30', false),
(2020, 3, 'T3', '2020-07-01', '2020-09-30', false),
(2020, 4, 'T4', '2020-10-01', '2020-12-31', false),
(2021, 1, 'T1', '2021-01-01', '2021-03-31', false),
(2021, 2, 'T2', '2021-04-01', '2021-06-30', false),
(2021, 3, 'T3', '2021-07-01', '2021-09-30', false),
(2021, 4, 'T4', '2021-10-01', '2021-12-31', false),
(2022, 1, 'T1', '2022-01-01', '2022-03-31', false),
(2022, 2, 'T2', '2022-04-01', '2022-06-30', false),
(2022, 3, 'T3', '2022-07-01', '2022-09-30', false),
(2022, 4, 'T4', '2022-10-01', '2022-12-31', false),
(2023, 1, 'T1', '2023-01-01', '2023-03-31', false),
(2023, 2, 'T2', '2023-04-01', '2023-06-30', false),
(2023, 3, 'T3', '2023-07-01', '2023-09-30', false),
(2023, 4, 'T4', '2023-10-01', '2023-12-31', false),
(2024, 1, 'T1', '2024-01-01', '2024-03-31', false),
(2024, 2, 'T2', '2024-04-01', '2024-06-30', false),
(2024, 3, 'T3', '2024-07-01', '2024-09-30', false),
(2024, 4, 'T4', '2024-10-01', '2024-12-31', true);

-- =============================================
-- COMMENTS FOR DOCUMENTATION
-- =============================================

COMMENT ON TABLE institutions IS 'Master table for Brazilian financial institutions based on BACEN registry';
COMMENT ON TABLE financial_data IS 'Main fact table storing all financial metrics from BACEN IFDATA';
COMMENT ON TABLE report_types IS 'Dimension table for the 13 BACEN report categories identified in EDA';
COMMENT ON TABLE metric_groups IS 'Dimension table for the 54 metric groups from BACEN taxonomy';
COMMENT ON TABLE metrics IS 'Dimension table for the 208 unique financial metrics identified';

COMMENT ON MATERIALIZED VIEW market_share_view IS 'Pre-calculated market share data for dashboard performance';
COMMENT ON MATERIALIZED VIEW institution_summary_view IS 'Institution overview optimized for detail pages';
COMMENT ON MATERIALIZED VIEW credit_portfolio_view IS 'Detailed credit portfolio analysis view';

-- Schema optimization complete
-- Ready for data migration and Supabase deployment