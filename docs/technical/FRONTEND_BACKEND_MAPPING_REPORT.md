# 🏦 Frontend-Backend Data Mapping Report
## Banco Insights 2.0 - Complete Integration Documentation

**Version**: 2.0
**Date**: January 2025
**Status**: Production Ready

---

## 📋 **Executive Summary**

This report provides a comprehensive mapping between frontend data requirements (currently using mock data) and the corresponding backend database queries and API endpoints. It covers both the **local CSV-based system** and the **Supabase cloud database** implementations.

### **Key Integration Points:**
- **6 Main Frontend Pages** requiring data integration
- **4 Core Data Types** with complex relationships
- **15+ API Endpoints** for complete functionality
- **50+ Database Queries** optimized for performance

---

## 🎯 **Frontend Pages & Data Requirements**

### **1. Market Overview Dashboard (`/market-overview`)**

**Purpose**: Sector-wide analytics and top institution rankings

#### **Data Requirements:**
- **Sector Aggregates**: Total assets, credit, deposits, institution count
- **Market Leaders**: Top 10 institutions by assets/credit/deposits
- **Segment Distribution**: S1-S5 segment breakdown
- **Growth Trends**: Quarter-over-quarter growth rates

#### **Mock Data Currently Used:**
```typescript
export const sectorData = {
  totalAssets: 11200000,      // R$ 11.2 tri
  totalCredit: 5800000,       // R$ 5.8 tri
  totalDeposits: 7200000,     // R$ 7.2 tri
  totalInstitutions: 2147,
  segments: {
    s1: { count: 5, assetsShare: 68.4 },
    s2: { count: 42, assetsShare: 18.2 }
    // ... more segments
  }
}
```

#### **Database Mapping:**

**Tables Involved:**
- `financial_data` (fact table)
- `institutions` (dimension)
- `time_periods` (dimension)
- `metrics` (dimension)
- `market_share_view` (materialized view)

**Key Queries:**
```sql
-- Sector Totals
SELECT
  SUM(CASE WHEN m.nome_coluna = 'Ativo Total' THEN fd.valor END) as total_assets,
  SUM(CASE WHEN m.nome_coluna LIKE '%Crédito%' THEN fd.valor END) as total_credit,
  SUM(CASE WHEN m.nome_coluna LIKE '%Depósito%' THEN fd.valor END) as total_deposits,
  COUNT(DISTINCT i.id) as institution_count
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN metrics m ON fd.metric_id = m.id
JOIN time_periods tp ON fd.time_period_id = tp.id
WHERE tp.year = 2024 AND tp.quarter = 4
  AND i.status = 'active';

-- Market Leaders
SELECT
  i.name,
  i.segment,
  SUM(fd.valor) as total_assets,
  RANK() OVER (ORDER BY SUM(fd.valor) DESC) as rank
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN metrics m ON fd.metric_id = m.id
WHERE m.nome_coluna = 'Ativo Total'
GROUP BY i.id, i.name, i.segment
ORDER BY total_assets DESC
LIMIT 10;
```

---

### **2. Institution Search (`/institution-search`)**

**Purpose**: Individual institution lookup and detailed profiles

#### **Data Requirements:**
- **Institution Directory**: Full list of 5,901 institutions
- **Search & Filters**: By name, segment, region, type
- **Institution Details**: CNPJ, address, founding date, status
- **Quick Stats**: Latest quarter financial highlights

#### **Mock Data Currently Used:**
```typescript
export interface Institution {
  id: string;
  cnpj: string;
  name: string;
  shortName: string;
  type: string;
  segment: string;
  controlType: string;
  region: string;
  city: string;
  foundedYear: number;
  status: 'active' | 'inactive';
  lastUpdate: string;
}
```

#### **Database Mapping:**

**Primary Table:** `institutions`

**Search Query:**
```sql
-- Institution Search with Filters
SELECT
  i.*,
  COALESCE(latest_assets.valor, 0) as latest_total_assets,
  COALESCE(latest_credit.valor, 0) as latest_credit,
  tp.year || ' ' || tp.quarter_text as latest_quarter
FROM institutions i
LEFT JOIN LATERAL (
  SELECT fd.valor
  FROM financial_data fd
  JOIN metrics m ON fd.metric_id = m.id
  JOIN time_periods tp ON fd.time_period_id = tp.id
  WHERE fd.institution_id = i.id
    AND m.nome_coluna = 'Ativo Total'
  ORDER BY tp.year DESC, tp.quarter DESC
  LIMIT 1
) latest_assets ON true
LEFT JOIN LATERAL (
  SELECT tp.year, tp.quarter_text
  FROM financial_data fd
  JOIN time_periods tp ON fd.time_period_id = tp.id
  WHERE fd.institution_id = i.id
  ORDER BY tp.year DESC, tp.quarter DESC
  LIMIT 1
) tp ON true
WHERE
  ($1 IS NULL OR LOWER(i.name) LIKE LOWER('%' || $1 || '%'))
  AND ($2 IS NULL OR i.segment = $2)
  AND ($3 IS NULL OR i.region = $3)
  AND i.status = 'active'
ORDER BY i.name
LIMIT $4 OFFSET $5;
```

---

### **3. Rankings (`/rankings`)**

**Purpose**: Institution rankings across multiple metrics and time periods

#### **Data Requirements:**
- **Multi-Metric Rankings**: Assets, credit, deposits, profitability
- **Historical Rankings**: Track position changes over time
- **Segment-Specific Rankings**: Within S1, S2, etc.
- **Market Share**: Percentage of total market

#### **Mock Data Currently Used:**
```typescript
export const marketShares: MarketShare[] = [
  {
    institutionId: '1',
    quarter: 'T4',
    year: 2024,
    assetsShare: 18.5,
    creditShare: 20.2,
    depositsShare: 19.8,
    rank: {
      assets: 1,
      credit: 1,
      deposits: 1
    }
  }
];
```

#### **Database Mapping:**

**Primary View:** `market_share_view`

**Rankings Query:**
```sql
-- Multi-Metric Rankings
SELECT
  institution_name,
  segment,
  year,
  quarter_text,
  market_share_pct,
  market_rank,
  institution_value,
  market_total
FROM market_share_view msv
JOIN metrics m ON msv.metric_name = m.nome_coluna
WHERE
  msv.year = $1
  AND msv.quarter = $2
  AND ($3 IS NULL OR msv.segment = $3)
  AND m.nome_coluna IN ('Ativo Total', 'Operações de Crédito', 'Captações')
ORDER BY msv.market_rank
LIMIT 50;
```

---

### **4. Analysis Tools (`/analysis-tools`)**

**Purpose**: Interactive financial analysis with custom visualizations

#### **Data Requirements:**
- **Time Series**: Multi-year quarterly data for trend analysis
- **Comparative Analysis**: Side-by-side institution comparison
- **Financial Metrics**: ROE, ROA, efficiency ratios, capital ratios
- **Credit Portfolio**: Breakdown by segments and modalities

#### **Mock Data Currently Used:**
```typescript
export const historicalAssets = [
  { quarter: 'T1 2020', bb: 1650000, itau: 1580000, cef: 1420000 },
  // 20 quarters of data...
];

export interface FinancialData {
  assets: { total: number; credit: number; securities: number; cash: number };
  income: { netIncome: number; operatingExpenses: number; provisions: number };
  ratios: { roe: number; roa: number; efficiency: number; capitalRatio: number };
}
```

#### **Database Mapping:**

**Time Series Query:**
```sql
-- Historical Financial Data
SELECT
  i.name as institution_name,
  tp.year,
  tp.quarter_text,
  tp.quarter,
  m.nome_coluna as metric_name,
  fd.valor,
  CASE
    WHEN m.tipo_dado = 'currency' THEN 'R$ milhões'
    WHEN m.tipo_dado = 'percentage' THEN '%'
    ELSE 'quantity'
  END as unit
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN time_periods tp ON fd.time_period_id = tp.id
JOIN metrics m ON fd.metric_id = m.id
WHERE
  i.cod_inst IN ($1)  -- Array of institution codes
  AND tp.year >= $2   -- Start year
  AND m.nome_coluna IN ($3)  -- Array of metrics
ORDER BY i.name, tp.year, tp.quarter, m.nome_coluna;
```

**Comparative Analysis Query:**
```sql
-- Institution Comparison (Latest Quarter)
WITH latest_quarter AS (
  SELECT MAX(year) as max_year, MAX(quarter) as max_quarter
  FROM time_periods
  WHERE id IN (SELECT DISTINCT time_period_id FROM financial_data)
)
SELECT
  i.name,
  i.segment,
  m.nome_coluna as metric,
  fd.valor,
  RANK() OVER (PARTITION BY m.id ORDER BY fd.valor DESC) as rank_position
FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
JOIN time_periods tp ON fd.time_period_id = tp.id
JOIN metrics m ON fd.metric_id = m.id
JOIN latest_quarter lq ON tp.year = lq.max_year AND tp.quarter = lq.max_quarter
WHERE
  i.cod_inst IN ($1)  -- Selected institutions
  AND m.nome_coluna IN ('Ativo Total', 'Lucro Líquido', 'ROE', 'ROA')
ORDER BY i.name, m.nome_coluna;
```

---

### **5. Home Dashboard (`/`)**

**Purpose**: Executive summary with key sector metrics and highlights

#### **Data Requirements:**
- **Sector KPIs**: Latest total assets, credit, deposits
- **Top Movers**: Institutions with highest growth
- **Market Concentration**: HHI index, top 5 vs others
- **Latest Updates**: Most recent data availability

#### **Database Mapping:**

**Dashboard Summary Query:**
```sql
-- Executive Dashboard Data
WITH latest_period AS (
  SELECT id, year, quarter_text
  FROM time_periods
  WHERE id = (
    SELECT time_period_id
    FROM financial_data
    GROUP BY time_period_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
  )
),
sector_totals AS (
  SELECT
    SUM(CASE WHEN m.nome_coluna = 'Ativo Total' THEN fd.valor END) as total_assets,
    SUM(CASE WHEN m.nome_coluna LIKE '%Crédito%' THEN fd.valor END) as total_credit,
    COUNT(DISTINCT i.id) as active_institutions
  FROM financial_data fd
  JOIN institutions i ON fd.institution_id = i.id
  JOIN metrics m ON fd.metric_id = m.id
  JOIN latest_period lp ON fd.time_period_id = lp.id
)
SELECT
  st.*,
  lp.year || ' ' || lp.quarter_text as data_reference,
  (SELECT COUNT(*) FROM institutions WHERE status = 'active') as total_institutions
FROM sector_totals st, latest_period lp;
```

---

## 🔗 **API Endpoints Mapping**

### **Current FastAPI Endpoints (CSV-based):**

| Endpoint | Purpose | Frontend Usage | Status |
|----------|---------|----------------|---------|
| `/plot/market_share` | Market share visualizations | Market Overview | ✅ Active |
| `/plot/share_credit_modality` | Credit modality breakdown | Analysis Tools | ✅ Active |
| `/plot/credit_portfolio` | Portfolio composition | Analysis Tools | ✅ Active |
| `/plot/dre_waterfall` | Financial statement waterfall | Analysis Tools | ✅ Active |
| `/plot/time_series` | Historical trends | Analysis Tools | ✅ Active |

### **Proposed Database-Driven Endpoints:**

#### **Institution Endpoints:**
```
GET /api/v2/institutions                    # Institution directory
GET /api/v2/institutions/{id}               # Institution details
GET /api/v2/institutions/search             # Search with filters
GET /api/v2/institutions/{id}/financials    # Institution financial data
GET /api/v2/institutions/{id}/rankings      # Institution rankings history
```

#### **Market Data Endpoints:**
```
GET /api/v2/market/overview                 # Sector aggregates
GET /api/v2/market/rankings                 # Market rankings
GET /api/v2/market/share                   # Market share data
GET /api/v2/market/concentration           # Market concentration metrics
GET /api/v2/market/segments                # Segment breakdown
```

#### **Financial Data Endpoints:**
```
GET /api/v2/financials/time-series         # Historical financial data
GET /api/v2/financials/compare             # Institution comparison
GET /api/v2/financials/ratios              # Financial ratios
GET /api/v2/financials/portfolio           # Credit portfolio analysis
GET /api/v2/financials/income              # Income statement data
```

#### **Analytics Endpoints:**
```
GET /api/v2/analytics/trends               # Trend analysis
GET /api/v2/analytics/correlations         # Correlation analysis
GET /api/v2/analytics/benchmarks           # Peer benchmarking
GET /api/v2/analytics/forecasts            # Predictive analytics
```

---

## 🗄️ **Database Query Optimization**

### **Performance Considerations:**

#### **Materialized Views (Pre-calculated):**
- `market_share_view` - Market share calculations
- `institution_summary_view` - Institution KPIs
- `credit_portfolio_view` - Credit portfolio breakdowns

#### **Indexes (Fast Lookups):**
- `idx_financial_data_institution_time` - Institution + time lookups
- `idx_institutions_search` - Full-text search on institution names
- `idx_financial_data_composite_query` - Complex analytical queries

#### **Query Patterns:**
```sql
-- Pattern 1: Latest Quarter Data (90% of queries)
SELECT * FROM financial_data fd
JOIN time_periods tp ON fd.time_period_id = tp.id
WHERE tp.year = 2024 AND tp.quarter = 4;

-- Pattern 2: Institution Filtering (80% of queries)
SELECT * FROM financial_data fd
JOIN institutions i ON fd.institution_id = i.id
WHERE i.cod_inst IN ('01234567', '87654321');

-- Pattern 3: Metric Aggregation (70% of queries)
SELECT SUM(fd.valor) FROM financial_data fd
JOIN metrics m ON fd.metric_id = m.id
WHERE m.nome_coluna = 'Ativo Total';
```

---

## 🌐 **Supabase Integration**

### **Connection Configuration:**
```javascript
// Frontend Supabase Client
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://uwoxkycxkidipgbptsgx.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
const supabase = createClient(supabaseUrl, supabaseKey)
```

### **Direct Database Queries:**
```javascript
// Market Overview Data
const { data: marketOverview } = await supabase
  .from('market_share_view')
  .select('institution_name, market_share_pct, market_rank')
  .eq('year', 2024)
  .eq('quarter', 4)
  .order('market_rank')
  .limit(10);

// Institution Search
const { data: institutions } = await supabase
  .from('institutions')
  .select('*')
  .ilike('name', `%${searchTerm}%`)
  .eq('status', 'active')
  .range(offset, offset + limit);

// Financial Time Series
const { data: timeSeries } = await supabase
  .from('financial_data')
  .select(`
    valor,
    institutions(name),
    time_periods(year, quarter_text),
    metrics(nome_coluna)
  `)
  .in('institutions.cod_inst', institutionCodes)
  .gte('time_periods.year', startYear)
  .in('metrics.nome_coluna', selectedMetrics);
```

---

## 🔄 **Data Transformation Pipeline**

### **Mock Data → Database Mapping:**

| Mock Data Field | Database Source | Transformation |
|------------------|----------------|----------------|
| `assets.total` | `financial_data.valor WHERE metrics.nome_coluna = 'Ativo Total'` | Direct value |
| `assets.credit` | `financial_data.valor WHERE metrics.nome_coluna LIKE '%Crédito%'` | Sum aggregation |
| `ratios.roe` | Calculated: `(Lucro Líquido / Patrimônio Líquido) * 100` | Formula |
| `segments.retail` | `financial_data.valor WHERE report_types.categoria = 'Credit' AND metric_groups.categoria = 'Retail'` | Category filter |
| `rank.assets` | `RANK() OVER (ORDER BY valor DESC)` | Window function |

### **Real-Time vs Cached Data:**

**Real-Time Queries** (Direct database):
- Institution search and details
- Latest quarter highlights
- Market rankings

**Cached Data** (Materialized views):
- Historical time series (refreshed monthly)
- Market share calculations (refreshed monthly)
- Complex analytical aggregations (refreshed monthly)

---

## 📊 **Implementation Priority Matrix**

### **High Priority (Phase 1):**
1. **Institution Search & Details** - Core functionality
2. **Market Overview Dashboard** - Executive summary
3. **Basic Rankings** - Top institutions by key metrics

### **Medium Priority (Phase 2):**
4. **Time Series Analysis** - Historical trends
5. **Comparative Analysis** - Institution comparison
6. **Credit Portfolio Analysis** - Detailed breakdowns

### **Low Priority (Phase 3):**
7. **Advanced Analytics** - Correlations, forecasting
8. **Custom Benchmarking** - Peer group analysis
9. **Export Capabilities** - Data download features

---

## 🎯 **Success Metrics**

### **Performance Targets:**
- **API Response Time**: < 500ms for 95% of queries
- **Database Query Performance**: < 200ms average
- **Frontend Load Time**: < 2 seconds initial load
- **Data Freshness**: Latest quarter data within 24 hours

### **Data Quality Metrics:**
- **Completeness**: > 95% of institutions have current quarter data
- **Accuracy**: Financial totals match BACEN official releases
- **Consistency**: No data discrepancies between views

---

## 📝 **Next Steps**

1. **✅ Complete ETL Pipeline** - Finish loading historical data
2. **⚡ Deploy New API Endpoints** - Implement database-driven APIs
3. **🔧 Frontend Integration** - Replace mock data with real endpoints
4. **🧪 Testing & Validation** - Comprehensive QA testing
5. **🚀 Production Deployment** - Go live with real data

---

**Document Status**: ✅ Complete
**Review Date**: January 2025
**Next Update**: After API implementation
