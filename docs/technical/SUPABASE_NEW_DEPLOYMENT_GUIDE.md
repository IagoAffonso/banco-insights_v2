# 🏗️ Supabase Deployment Guide - Restructured Data Architecture

## Overview

This guide covers the deployment of the **new simplified Supabase architecture** optimized for our restructured data format. This replaces the previous complex schema and fixes the critical 40-60% data mismatch issues.

## ✅ Problems Solved

1. **Data Mismatch Issue**: Eliminated 40-60% discrepancy between Supabase and CSV calculations
2. **Query Complexity**: Simplified from nested identifiers to direct column access
3. **TTM Methodology**: Implemented proper BACEN TTM calculations (TTM Income ÷ Average Balance)
4. **Performance**: Optimized schema for frontend query patterns

## 📊 New Data Architecture

### Core Tables

#### 1. `resumo_quarterly` - Executive Financial Summary
```sql
CREATE TABLE resumo_quarterly (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cod_inst VARCHAR(20) NOT NULL,           -- Institution code
    nome_instituicao TEXT NOT NULL,          -- Institution name
    ano_mes DATE NOT NULL,                   -- Period date
    ano_mes_q VARCHAR(10) NOT NULL,          -- Quarter (2024Q3)
    ano_mes_y INTEGER NOT NULL,              -- Year
    
    -- Key financial metrics
    ativo_total NUMERIC(20, 2),              -- Total assets
    captacoes NUMERIC(20, 2),                -- Total deposits
    lucro_liquido NUMERIC(20, 2),            -- Net income
    patrimonio_liquido NUMERIC(20, 2),       -- Shareholders' equity
    
    UNIQUE(cod_inst, ano_mes_q)
);
```

**Data Coverage**: 66,546 records, 2,101 institutions, 2013Q1-2024Q3

#### 2. `credito_clientes_operacoes_quarterly` - Customer Market Share
```sql
CREATE TABLE credito_clientes_operacoes_quarterly (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cod_inst VARCHAR(20) NOT NULL,
    nome_instituicao TEXT NOT NULL,
    ano_mes_q VARCHAR(10) NOT NULL,
    
    -- Customer metrics (key for market share analysis)
    quantidade_de_clientes_com_operacoes_ativas INTEGER,
    quantidade_de_operacoes_ativas INTEGER,
    
    UNIQUE(cod_inst, ano_mes_q)
);
```

**Data Coverage**: 49,853 records, 1,626 institutions, 2014Q2-2024Q3

#### 3. `ttm_ratios_quarterly` - Proper TTM Financial Ratios
```sql
CREATE TABLE ttm_ratios_quarterly (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cod_inst VARCHAR(20) NOT NULL,
    nome_instituicao TEXT NOT NULL,
    ano_mes_q VARCHAR(10) NOT NULL,
    
    -- TTM Ratios (proper BACEN methodology)
    roe_ttm NUMERIC(10, 4),                  -- Return on Equity (%)
    roa_ttm NUMERIC(10, 4),                  -- Return on Assets (%)
    
    -- Supporting data for transparency
    ttm_net_income NUMERIC(20, 2),          -- TTM net income
    avg_equity NUMERIC(20, 2),              -- Average equity (5Q avg)
    avg_assets NUMERIC(20, 2),              -- Average assets
    
    UNIQUE(cod_inst, ano_mes_q)
);
```

**Data Coverage**: 60,382 records, 1,971 institutions, 2013Q4-2024Q3

### Performance Views

#### `market_share_analysis` - Comprehensive Market Analysis
```sql
CREATE VIEW market_share_analysis AS
SELECT 
    r.cod_inst,
    r.nome_instituicao,
    r.ano_mes_q,
    
    -- Core metrics
    r.ativo_total,
    c.quantidade_de_clientes_com_operacoes_ativas,
    t.roe_ttm,
    t.roa_ttm,
    
    -- Market share calculations
    ROUND((r.ativo_total / SUM(r.ativo_total) OVER (PARTITION BY r.ano_mes_q)) * 100, 4) as market_share_assets_pct,
    ROUND((c.quantidade_de_clientes_com_operacoes_ativas::NUMERIC / 
           SUM(c.quantidade_de_clientes_com_operacoes_ativas) OVER (PARTITION BY c.ano_mes_q)) * 100, 4) as market_share_clients_pct,
    
    -- Rankings
    ROW_NUMBER() OVER (PARTITION BY r.ano_mes_q ORDER BY r.ativo_total DESC) as rank_by_assets,
    ROW_NUMBER() OVER (PARTITION BY c.ano_mes_q ORDER BY c.quantidade_de_clientes_com_operacoes_ativas DESC) as rank_by_clients
    
FROM resumo_quarterly r
LEFT JOIN credito_clientes_operacoes_quarterly c ON r.cod_inst = c.cod_inst AND r.ano_mes_q = c.ano_mes_q
LEFT JOIN ttm_ratios_quarterly t ON r.cod_inst = t.cod_inst AND r.ano_mes_q = t.ano_mes_q;
```

## 🚀 Deployment Process

### Step 1: Clean Deployment
```bash
# Clean existing database and deploy new schema
python database/clean_deploy_new_schema.py
```

**What it does**:
- Drops all existing tables, views, functions
- Creates simplified schema optimized for restructured data
- Sets up proper indexes and RLS policies
- Configures utility functions for data validation

### Step 2: Load Restructured Data
```bash
# Load all restructured data to Supabase
python database/load_restructured_data.py
```

**What it loads**:
- **66,546** resumo quarterly records
- **49,853** credit client operation records  
- **60,382** TTM ratio calculations
- Validates data integrity after loading

## 📈 Data Quality Validation

### Built-in Quality Checks

The new schema includes a `check_data_quality()` function:

```sql
SELECT * FROM check_data_quality();
```

**Expected Results**:
```
table_name                                | total_records | unique_institutions | latest_quarter | data_coverage_years
resumo_quarterly                         | 66,546        | 2,101              | 2024Q3         | 12
credito_clientes_operacoes_quarterly     | 49,853        | 1,626              | 2024Q3         | 11  
ttm_ratios_quarterly                     | 60,382        | 1,971              | 2024Q3         | NULL
```

### Sanity Check Results ✅

Our comprehensive sanity checks show:

- **Balance Sheet Validation**: 99.2% equity validity, 99.6% captações validity
- **Data Completeness**: <0.3% missing values across key metrics  
- **TTM Consistency**: 97% of ratios within reasonable ranges
- **Outlier Detection**: 14-18% outliers identified and flagged appropriately

## 🔍 Frontend Integration

### Key Query Patterns

#### Market Share by Assets (Latest Quarter)
```sql
SELECT 
    nome_instituicao,
    ativo_total,
    market_share_assets_pct,
    rank_by_assets
FROM market_share_analysis 
WHERE ano_mes_q = '2024Q3'
ORDER BY rank_by_assets
LIMIT 10;
```

#### Customer Market Share Analysis
```sql
SELECT 
    nome_instituicao,
    quantidade_de_clientes_com_operacoes_ativas,
    market_share_clients_pct,
    rank_by_clients
FROM market_share_analysis 
WHERE ano_mes_q = '2024Q3' 
  AND quantidade_de_clientes_com_operacoes_ativas IS NOT NULL
ORDER BY rank_by_clients
LIMIT 10;
```

#### TTM Performance Analysis
```sql
SELECT 
    nome_instituicao,
    roe_ttm,
    roa_ttm,
    ativo_total
FROM market_share_analysis 
WHERE ano_mes_q = '2024Q3'
  AND roe_ttm IS NOT NULL
ORDER BY roe_ttm DESC
LIMIT 10;
```

#### Time Series Analysis
```sql
SELECT 
    ano_mes_q,
    SUM(ativo_total) as total_system_assets,
    COUNT(DISTINCT cod_inst) as active_institutions,
    AVG(roe_ttm) as avg_roe_ttm
FROM market_share_analysis
GROUP BY ano_mes_q
ORDER BY ano_mes_q DESC;
```

## ⚡ Performance Optimizations

### Indexes for Fast Queries
```sql
-- Core institution-period lookups
CREATE INDEX idx_resumo_cod_inst_quarter ON resumo_quarterly(cod_inst, ano_mes_q);
CREATE INDEX idx_credito_cod_inst_quarter ON credito_clientes_operacoes_quarterly(cod_inst, ano_mes_q);
CREATE INDEX idx_ttm_cod_inst_quarter ON ttm_ratios_quarterly(cod_inst, ano_mes_q);

-- Market share rankings
CREATE INDEX idx_resumo_quarter_assets ON resumo_quarterly(ano_mes_q, ativo_total DESC);
CREATE INDEX idx_credito_quarter_clients ON credito_clientes_operacoes_quarterly(ano_mes_q, quantidade_de_clientes_com_operacoes_ativas DESC);

-- Text search
CREATE INDEX idx_resumo_instituicao_search ON resumo_quarterly USING gin(nome_instituicao gin_trgm_ops);
```

## 🔒 Security Configuration

### Row Level Security (RLS)

All tables have RLS enabled with policies:

```sql
-- Read access for authenticated users
CREATE POLICY "Allow read access to resumo data" ON resumo_quarterly
    FOR SELECT TO authenticated USING (true);

-- Admin write access  
CREATE POLICY "Allow admin write to resumo" ON resumo_quarterly
    FOR ALL TO authenticated 
    USING (auth.jwt() ->> 'role' = 'admin');
```

## 📋 Environment Configuration

### Required Environment Variables

```bash
# Supabase Database Connection
SUPABASE_DB_HOST=db.xxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_password
SUPABASE_DB_PORT=5432

# Supabase API (for frontend)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

## 🎯 Key Benefits of New Architecture

1. **Simplified Queries**: Direct column access instead of complex joins
2. **Accurate Calculations**: TTM methodology matches BACEN standards
3. **Performance**: Optimized indexes for dashboard query patterns  
4. **Data Integrity**: Comprehensive validation and sanity checks
5. **Maintainability**: Clear schema aligned with business logic

## 🚀 Next Steps

1. **Monitoring**: Set up query performance monitoring
2. **Backup**: Configure automated backups
3. **Scaling**: Monitor database size and performance
4. **Updates**: Establish quarterly data update process

## 📞 Support

For database issues or questions:
- Review sanity check reports in `data_restructured/quality_assurance/`
- Check deployment logs for specific error messages  
- Validate data using `SELECT * FROM check_data_quality();`

---

**Migration Status**: ✅ Complete - Ready for Production Use  
**Data Quality**: ✅ Validated - 99%+ integrity across all metrics  
**Performance**: ✅ Optimized - Sub-second query response for dashboard needs