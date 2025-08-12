# 📊 Restructured Data Directory

**Purpose**: Contains transposed, query-friendly CSV tables derived from `consolidated_cleaned.csv`  
**Created**: January 2025  
**Format**: Wide-format tables with metrics as columns instead of row identifiers

---

## 📁 Folder Structure

### **core_tables/** 
Core financial reports with standardized column structure:
- `resumo_quarterly.csv` - Executive summary metrics
- `ativo_quarterly.csv` - Balance sheet assets  
- `passivo_quarterly.csv` - Balance sheet liabilities
- `demonstracao_resultado_quarterly.csv` - Income statement (P&L)
- `informacoes_capital_quarterly.csv` - Regulatory capital & Basel metrics

### **credit_tables/**
Credit portfolio analysis tables:
- `credito_indexador_quarterly.csv` - Credit by interest rate indexer
- `credito_risco_quarterly.csv` - Credit by risk level (AA-H)
- `credito_regiao_quarterly.csv` - Credit by geographic region  
- `credito_pf_modalidade_quarterly.csv` - Individual credit by modality
- `credito_pj_modalidade_quarterly.csv` - Corporate credit by modality
- `credito_pj_cnae_quarterly.csv` - Corporate credit by economic sector
- `credito_pj_porte_quarterly.csv` - Corporate credit by company size
- `credito_clientes_operacoes_quarterly.csv` - Client and operation counts

### **calculated_metrics/**
Derived metrics and ratios:
- `performance_ratios_quarterly.csv` - ROE, ROA, efficiency ratios
- `market_share_quarterly.csv` - Institution vs market percentages
- `growth_rates_quarterly.csv` - QoQ, YoY growth calculations
- `financial_ratios_quarterly.csv` - Credit/deposit, cost/income ratios

### **market_analysis/**
Market-level aggregations and analytics:
- `market_totals_quarterly.csv` - Sector-wide totals by period
- `concentration_metrics_quarterly.csv` - HHI and concentration indices
- `peer_groups_quarterly.csv` - Institution classifications and benchmarks

---

## 🔧 Table Structure Standards

### Common Columns (All Tables)
```
CodInst          - 8-digit institution identifier
NomeInstituicao  - Institution name
AnoMes          - Date (YYYY-MM-DD format)  
AnoMes_Q        - Quarterly period (2024Q3)
AnoMes_Y        - Yearly period (2024)
```

### Naming Convention
- **Snake_case**: All metric columns use underscores
- **No_spaces**: Spaces replaced with underscores  
- **Descriptive**: Business meaning preserved
- **Consistent**: Related metrics grouped with prefixes

### Example Column Names
```
Ativo_Total
Lucro_Liquido  
Indice_de_Basileia
Receitas_de_Intermediacao_Financeira
Quantidade_de_Clientes_com_Operacoes_Ativas
```

---

## 📈 Data Quality Features

### Validation
- **Balance Sheet**: Assets = Liabilities + Equity
- **P&L Integrity**: Revenue components sum correctly
- **Basel Compliance**: Capital ratios within bounds
- **Source Mapping**: Each column traced to original identifier

### Auditing
- **Calculation Documentation**: All formulas documented
- **Data Lineage**: Transformation process tracked  
- **Quality Metrics**: Missing data rates monitored
- **Outlier Detection**: Automated anomaly identification

---

## 🚀 Usage Examples

### Simple Queries
```python
# Load core financial data
df = pd.read_csv('core_tables/resumo_quarterly.csv')

# Get total assets for institution 12345 in Q3 2024
assets = df[(df['CodInst'] == '12345') & 
           (df['AnoMes_Q'] == '2024Q3')]['Ativo_Total'].iloc[0]
```

### Market Analysis
```python
# Load market share data  
ms = pd.read_csv('calculated_metrics/market_share_quarterly.csv')

# Top 10 institutions by asset market share
top10 = ms[ms['AnoMes_Q'] == '2024Q3'].nlargest(10, 'Market_Share_Ativo_Total')
```

### Performance Analysis
```python  
# Load performance ratios
pr = pd.read_csv('calculated_metrics/performance_ratios_quarterly.csv')

# ROE trend analysis
roe_trend = pr[pr['CodInst'] == '12345'][['AnoMes_Q', 'ROE']].sort_values('AnoMes_Q')
```

---

## 🔗 Integration Points

### API Endpoints
Tables designed for RESTful API integration:
```
GET /api/v1/institutions/{cod_inst}/summary?period={quarter}
GET /api/v1/market-share/{metric}?period={quarter}  
GET /api/v1/credit-portfolio/{institution}/{modality}
```

### Dashboard Components
- **Summary Cards**: Direct column mapping from resumo_quarterly.csv
- **Time Series**: Multi-period analysis across quarters
- **Peer Comparison**: Cross-institutional benchmarking
- **Market Share**: Competitive positioning analysis

### Database Migration
Tables ready for PostgreSQL/Supabase import:
- **Indexes**: Composite indexes on (CodInst, AnoMes)
- **Constraints**: Foreign key relationships preserved
- **Views**: Materialized views for complex aggregations

---

## 📋 File Naming Convention

### Pattern: `{report_type}_{frequency}.csv`
- **report_type**: Descriptive table name (resumo, ativo, credito_risco)
- **frequency**: Data frequency (quarterly, annual)
- **Examples**: 
  - `resumo_quarterly.csv`
  - `credito_pf_modalidade_quarterly.csv` 
  - `market_share_quarterly.csv`

---

## ⚡ Performance Benefits

### Query Speed
- **10x Faster**: Direct column access vs string filtering
- **Index Friendly**: Optimized for database indexing
- **Join Efficient**: Simple primary key relationships

### Development Speed  
- **React Components**: Direct API to UI mapping
- **SQL Queries**: Standard WHERE clauses
- **Analytics**: Native pandas/numpy operations

### Maintenance
- **Schema Clarity**: Self-documenting column names
- **Type Safety**: Consistent data types per column
- **Version Control**: Easy to track schema changes

---

**Status**: Ready for implementation ✅  
**Next Steps**: Generate transformation scripts and populate tables