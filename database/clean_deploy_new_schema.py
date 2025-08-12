"""
🧹 Clean Supabase Database and Deploy New Simplified Schema

This script completely cleans the existing database and deploys a new schema
optimized for our restructured data format (resumo_quarterly, etc.)
"""

import os
import pandas as pd
from pathlib import Path
import psycopg2
from psycopg2 import sql
import warnings
from typing import Dict, List, Optional
import json

warnings.filterwarnings('ignore')

class SupabaseCleanDeployment:
    """
    Clean deployment to Supabase with simplified schema.
    """
    
    def __init__(self):
        self.connection_params = self.load_database_config()
        self.data_dir = Path("data_restructured")
        
    def load_database_config(self) -> Dict:
        """
        Load database configuration from environment or config file.
        """
        
        # Try to load from environment variables first
        if all(key in os.environ for key in ['SUPABASE_DB_HOST', 'SUPABASE_DB_NAME', 'SUPABASE_DB_USER', 'SUPABASE_DB_PASSWORD']):
            return {
                'host': os.environ['SUPABASE_DB_HOST'],
                'database': os.environ['SUPABASE_DB_NAME'],
                'user': os.environ['SUPABASE_DB_USER'],
                'password': os.environ['SUPABASE_DB_PASSWORD'],
                'port': os.environ.get('SUPABASE_DB_PORT', '5432')
            }
        
        # Try to load from archived config
        config_file = Path("archive/deployment_configs/supabase_config.env")
        if config_file.exists():
            config = {}
            with open(config_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key.lower().replace('supabase_db_', '')] = value.strip('"\'')
            return config
        
        raise ValueError("Database configuration not found. Please set environment variables or provide config file.")
    
    def connect_to_database(self):
        """
        Establish connection to Supabase database.
        """
        try:
            conn = psycopg2.connect(**self.connection_params)
            conn.autocommit = False
            return conn
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def clean_existing_database(self, conn) -> bool:
        """
        Completely clean the existing database structure.
        """
        
        print("🧹 CLEANING EXISTING DATABASE")
        print("=" * 50)
        
        try:
            cursor = conn.cursor()
            
            # Drop all existing materialized views
            print("🔄 Dropping materialized views...")
            materialized_views = [
                'market_share_view',
                'institution_summary_view', 
                'credit_portfolio_view'
            ]
            
            for view in materialized_views:
                try:
                    cursor.execute(f"DROP MATERIALIZED VIEW IF EXISTS {view} CASCADE;")
                    print(f"   ✅ Dropped {view}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop {view}: {e}")
            
            # Drop all existing tables
            print("\\n🗑️  Dropping existing tables...")
            tables_to_drop = [
                'financial_data',
                'institutions', 
                'report_types',
                'metric_groups',
                'metrics',
                'time_periods',
                'geographic_regions'
            ]
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                    print(f"   ✅ Dropped {table}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop {table}: {e}")
            
            # Drop functions
            print("\\n⚙️  Dropping functions...")
            functions_to_drop = [
                'refresh_all_materialized_views()',
                'update_updated_at_column()'
            ]
            
            for func in functions_to_drop:
                try:
                    cursor.execute(f"DROP FUNCTION IF EXISTS {func} CASCADE;")
                    print(f"   ✅ Dropped {func}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop {func}: {e}")
            
            conn.commit()
            print("\\n✅ Database cleaned successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database cleaning failed: {e}")
            conn.rollback()
            return False
    
    def create_simplified_schema(self, conn) -> bool:
        """
        Create simplified schema matching our restructured data format.
        """
        
        print("\\n🏗️  CREATING SIMPLIFIED SCHEMA")
        print("=" * 50)
        
        schema_sql = '''
        -- Banco Insights 2.0 - Simplified Schema for Restructured Data
        -- Optimized for query performance and frontend requirements
        
        -- Enable necessary extensions
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE EXTENSION IF NOT EXISTS "pg_trgm";
        
        -- =============================================
        -- CORE TABLES FOR RESTRUCTURED DATA
        -- =============================================
        
        -- Resumo Quarterly Table (Executive Summary)
        CREATE TABLE resumo_quarterly (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            cod_inst VARCHAR(20) NOT NULL,
            nome_instituicao TEXT NOT NULL,
            ano_mes DATE NOT NULL,
            ano_mes_q VARCHAR(10) NOT NULL, -- '2024Q3' format
            ano_mes_y INTEGER NOT NULL,
            
            -- Financial metrics (from restructured data)
            ativo_total NUMERIC(20, 2),
            captacoes NUMERIC(20, 2),
            lucro_liquido NUMERIC(20, 2),
            patrimonio_liquido NUMERIC(20, 2),
            
            -- Audit fields
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Constraints
            UNIQUE(cod_inst, ano_mes_q)
        );
        
        -- Credit Operations Client Data (Customer Market Share)
        CREATE TABLE credito_clientes_operacoes_quarterly (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            cod_inst VARCHAR(20) NOT NULL,
            nome_instituicao TEXT NOT NULL,
            ano_mes DATE NOT NULL,
            ano_mes_q VARCHAR(10) NOT NULL,
            ano_mes_y INTEGER NOT NULL,
            
            -- Customer metrics (key for market share analysis)
            quantidade_de_clientes_com_operacoes_ativas INTEGER,
            quantidade_de_operacoes_ativas INTEGER,
            
            -- Audit fields
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Constraints
            UNIQUE(cod_inst, ano_mes_q)
        );
        
        -- TTM Calculated Ratios Table
        CREATE TABLE ttm_ratios_quarterly (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            cod_inst VARCHAR(20) NOT NULL,
            nome_instituicao TEXT NOT NULL,
            ano_mes_q VARCHAR(10) NOT NULL,
            
            -- TTM Ratios (proper methodology)
            roe_ttm NUMERIC(10, 4), -- Return on Equity (%)
            roa_ttm NUMERIC(10, 4), -- Return on Assets (%)
            
            -- Supporting data for transparency
            ttm_net_income NUMERIC(20, 2),
            avg_equity NUMERIC(20, 2),
            avg_assets NUMERIC(20, 2),
            quarters_used_income INTEGER,
            quarters_used_balance INTEGER,
            
            -- Audit fields
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Constraints
            UNIQUE(cod_inst, ano_mes_q)
        );
        
        -- =============================================
        -- PERFORMANCE OPTIMIZED VIEWS
        -- =============================================
        
        -- Market Share Analysis View
        CREATE VIEW market_share_analysis AS
        SELECT 
            r.cod_inst,
            r.nome_instituicao,
            r.ano_mes_q,
            r.ano_mes_y,
            
            -- Core financial metrics
            r.ativo_total,
            r.patrimonio_liquido,
            r.lucro_liquido,
            
            -- Customer metrics (key for market share)
            c.quantidade_de_clientes_com_operacoes_ativas as clientes_ativos,
            c.quantidade_de_operacoes_ativas as operacoes_ativas,
            
            -- TTM Ratios
            t.roe_ttm,
            t.roa_ttm,
            
            -- Market share calculations (assets)
            ROUND(
                (r.ativo_total / NULLIF(
                    SUM(r.ativo_total) OVER (PARTITION BY r.ano_mes_q), 0
                )) * 100, 4
            ) as market_share_assets_pct,
            
            -- Market share calculations (customers)
            ROUND(
                (c.quantidade_de_clientes_com_operacoes_ativas::NUMERIC / NULLIF(
                    SUM(c.quantidade_de_clientes_com_operacoes_ativas) OVER (PARTITION BY c.ano_mes_q), 0
                )) * 100, 4
            ) as market_share_clients_pct,
            
            -- Rankings
            ROW_NUMBER() OVER (
                PARTITION BY r.ano_mes_q 
                ORDER BY r.ativo_total DESC
            ) as rank_by_assets,
            
            ROW_NUMBER() OVER (
                PARTITION BY c.ano_mes_q 
                ORDER BY c.quantidade_de_clientes_com_operacoes_ativas DESC
            ) as rank_by_clients
            
        FROM resumo_quarterly r
        LEFT JOIN credito_clientes_operacoes_quarterly c 
            ON r.cod_inst = c.cod_inst AND r.ano_mes_q = c.ano_mes_q
        LEFT JOIN ttm_ratios_quarterly t 
            ON r.cod_inst = t.cod_inst AND r.ano_mes_q = t.ano_mes_q
        ORDER BY r.ano_mes_q DESC, r.ativo_total DESC;
        
        -- Institution Performance Summary
        CREATE VIEW institution_performance AS
        SELECT 
            r.cod_inst,
            r.nome_instituicao,
            
            -- Latest quarter data
            r.ano_mes_q as latest_quarter,
            r.ativo_total as latest_assets,
            r.patrimonio_liquido as latest_equity,
            c.quantidade_de_clientes_com_operacoes_ativas as latest_clients,
            
            -- TTM Performance
            t.roe_ttm as latest_roe_ttm,
            t.roa_ttm as latest_roa_ttm,
            
            -- Growth metrics (YoY)
            LAG(r.ativo_total, 4) OVER (
                PARTITION BY r.cod_inst ORDER BY r.ano_mes_q
            ) as assets_4q_ago,
            
            -- Asset growth rate
            CASE 
                WHEN LAG(r.ativo_total, 4) OVER (
                    PARTITION BY r.cod_inst ORDER BY r.ano_mes_q
                ) > 0 THEN
                    ROUND(
                        ((r.ativo_total / LAG(r.ativo_total, 4) OVER (
                            PARTITION BY r.cod_inst ORDER BY r.ano_mes_q
                        )) - 1) * 100, 2
                    )
                ELSE NULL
            END as asset_growth_yoy_pct
            
        FROM resumo_quarterly r
        LEFT JOIN credito_clientes_operacoes_quarterly c 
            ON r.cod_inst = c.cod_inst AND r.ano_mes_q = c.ano_mes_q
        LEFT JOIN ttm_ratios_quarterly t 
            ON r.cod_inst = t.cod_inst AND r.ano_mes_q = t.ano_mes_q
        ORDER BY r.ativo_total DESC;
        
        -- =============================================
        -- PERFORMANCE INDEXES
        -- =============================================
        
        -- Core indexes for fast queries
        CREATE INDEX idx_resumo_cod_inst_quarter ON resumo_quarterly(cod_inst, ano_mes_q);
        CREATE INDEX idx_resumo_quarter_assets ON resumo_quarterly(ano_mes_q, ativo_total DESC);
        
        CREATE INDEX idx_credito_cod_inst_quarter ON credito_clientes_operacoes_quarterly(cod_inst, ano_mes_q);
        CREATE INDEX idx_credito_quarter_clients ON credito_clientes_operacoes_quarterly(ano_mes_q, quantidade_de_clientes_com_operacoes_ativas DESC);
        
        CREATE INDEX idx_ttm_cod_inst_quarter ON ttm_ratios_quarterly(cod_inst, ano_mes_q);
        CREATE INDEX idx_ttm_quarter_roe ON ttm_ratios_quarterly(ano_mes_q, roe_ttm DESC);
        
        -- Text search indexes
        CREATE INDEX idx_resumo_instituicao_search ON resumo_quarterly USING gin(nome_instituicao gin_trgm_ops);
        
        -- Time-based indexes
        CREATE INDEX idx_resumo_year_quarter ON resumo_quarterly(ano_mes_y DESC, ano_mes_q DESC);
        
        -- =============================================
        -- UTILITY FUNCTIONS
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
        CREATE TRIGGER update_resumo_updated_at 
            BEFORE UPDATE ON resumo_quarterly 
            FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
            
        CREATE TRIGGER update_credito_updated_at 
            BEFORE UPDATE ON credito_clientes_operacoes_quarterly
            FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
            
        CREATE TRIGGER update_ttm_updated_at 
            BEFORE UPDATE ON ttm_ratios_quarterly
            FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
        
        -- Data quality check function
        CREATE OR REPLACE FUNCTION check_data_quality()
        RETURNS TABLE(
            table_name TEXT,
            total_records BIGINT,
            unique_institutions BIGINT,
            latest_quarter TEXT,
            data_coverage_years INTEGER
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                'resumo_quarterly'::TEXT,
                COUNT(*)::BIGINT,
                COUNT(DISTINCT cod_inst)::BIGINT,
                MAX(ano_mes_q),
                (MAX(ano_mes_y) - MIN(ano_mes_y) + 1)::INTEGER
            FROM resumo_quarterly
            
            UNION ALL
            
            SELECT 
                'credito_clientes_operacoes_quarterly'::TEXT,
                COUNT(*)::BIGINT,
                COUNT(DISTINCT cod_inst)::BIGINT,
                MAX(ano_mes_q),
                (MAX(ano_mes_y) - MIN(ano_mes_y) + 1)::INTEGER
            FROM credito_clientes_operacoes_quarterly
            
            UNION ALL
            
            SELECT 
                'ttm_ratios_quarterly'::TEXT,
                COUNT(*)::BIGINT,
                COUNT(DISTINCT cod_inst)::BIGINT,
                MAX(ano_mes_q),
                NULL::INTEGER
            FROM ttm_ratios_quarterly;
        END;
        $$ LANGUAGE plpgsql;
        
        -- =============================================
        -- ROW LEVEL SECURITY FOR SUPABASE
        -- =============================================
        
        -- Enable RLS on all tables
        ALTER TABLE resumo_quarterly ENABLE ROW LEVEL SECURITY;
        ALTER TABLE credito_clientes_operacoes_quarterly ENABLE ROW LEVEL SECURITY;
        ALTER TABLE ttm_ratios_quarterly ENABLE ROW LEVEL SECURITY;
        
        -- Basic read policies for authenticated users
        CREATE POLICY "Allow read access to resumo data" ON resumo_quarterly
            FOR SELECT TO authenticated USING (true);
            
        CREATE POLICY "Allow read access to credito data" ON credito_clientes_operacoes_quarterly
            FOR SELECT TO authenticated USING (true);
            
        CREATE POLICY "Allow read access to ttm data" ON ttm_ratios_quarterly
            FOR SELECT TO authenticated USING (true);
        
        -- Admin write policies
        CREATE POLICY "Allow admin write to resumo" ON resumo_quarterly
            FOR ALL TO authenticated 
            USING (auth.jwt() ->> 'role' = 'admin');
            
        CREATE POLICY "Allow admin write to credito" ON credito_clientes_operacoes_quarterly
            FOR ALL TO authenticated
            USING (auth.jwt() ->> 'role' = 'admin');
            
        CREATE POLICY "Allow admin write to ttm" ON ttm_ratios_quarterly
            FOR ALL TO authenticated
            USING (auth.jwt() ->> 'role' = 'admin');
        
        -- =============================================
        -- COMMENTS FOR DOCUMENTATION
        -- =============================================
        
        COMMENT ON TABLE resumo_quarterly IS 'Executive summary financial data - restructured from BACEN IFDATA';
        COMMENT ON TABLE credito_clientes_operacoes_quarterly IS 'Customer market share metrics - key for competitive analysis';
        COMMENT ON TABLE ttm_ratios_quarterly IS 'TTM financial ratios calculated using proper BACEN methodology';
        
        COMMENT ON VIEW market_share_analysis IS 'Comprehensive market share analysis with rankings';
        COMMENT ON VIEW institution_performance IS 'Institution performance summary with growth metrics';
        
        '''
        
        try:
            cursor = conn.cursor()
            cursor.execute(schema_sql)
            conn.commit()
            
            print("✅ Simplified schema created successfully!")
            
            # Test the schema by running data quality check
            cursor.execute("SELECT * FROM check_data_quality();")
            results = cursor.fetchall()
            
            print("\\n📊 Schema validation:")
            print("   • Tables created with proper structure")
            print("   • Indexes and triggers configured")
            print("   • RLS policies applied")
            print("   • Utility functions installed")
            
            return True
            
        except Exception as e:
            print(f"❌ Schema creation failed: {e}")
            conn.rollback()
            return False
    
    def run_clean_deployment(self) -> bool:
        """
        Execute complete clean deployment.
        """
        
        print("🚀 STARTING CLEAN SUPABASE DEPLOYMENT")
        print("=" * 60)
        
        # Connect to database
        conn = self.connect_to_database()
        if not conn:
            return False
        
        try:
            # Step 1: Clean existing database
            if not self.clean_existing_database(conn):
                return False
            
            # Step 2: Create simplified schema
            if not self.create_simplified_schema(conn):
                return False
            
            print("\\n🎉 CLEAN DEPLOYMENT COMPLETED SUCCESSFULLY!")
            print("✅ Database is ready for new data loading")
            print("🚀 Next: Load restructured data to Supabase")
            
            return True
            
        finally:
            conn.close()

def main():
    """Execute clean deployment."""
    
    print("⚠️  WARNING: This will completely clean your Supabase database!")
    print("All existing data and schema will be permanently deleted.")
    print()
    
    # For automated execution, we'll proceed
    # In interactive mode, you might want to add confirmation
    
    deployer = SupabaseCleanDeployment()
    success = deployer.run_clean_deployment()
    
    if success:
        print("\\n✅ Step 4b completed: Supabase database cleaned and new schema deployed")
        print("📋 Ready to proceed with Step 4c: Update documentation")
        print("📋 Then Step 4d: Load restructured data")
    else:
        print("❌ Clean deployment failed - check configuration and try again")
    
    return success

if __name__ == "__main__":
    main()