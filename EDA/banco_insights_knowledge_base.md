# 🏦 Banco Insights 2.0 - Complete Knowledge Base

**Version**: 2.0  
**Last Updated**: January 2025  
**Purpose**: Comprehensive understanding of BACEN data pipeline, ETL processes, and database architecture

---

## 📋 Executive Summary

This knowledge base documents the complete data architecture and processing pipeline for Banco Insights 2.0, a Brazilian banking sector intelligence platform that analyzes data from 2,000+ financial institutions regulated by BACEN (Central Bank of Brazil). The platform processes quarterly reports from 2013-2024, providing market analysis, benchmarks, and financial insights.

---

## 🗂️ Data Architecture Overview

### 🔍 Data Flow Hierarchy

```
Raw Data (BACEN API) → ETL Processing → Consolidated Datasets → Specialized Views → Application Layer
```

### 1. **Raw Data Layer** 📊

**Location**: `bacen_project_v1/data/data_raw_reports/`

**Structure**: Individual quarterly CSV files following the pattern:
- `data_YYYYMM_Tipo2_RelatorioT.csv`
- **Example**: `data_202403_Tipo2_RelatorioT.csv` (March 2024)
- **Coverage**: Q1 2013 to Q3 2024 (47+ quarterly files)
- **Size**: Each file contains thousands of records per quarter

**Source**: BACEN IFDATA API (`fetch_data.py`)
- **Endpoint**: `https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata`
- **Report Type**: Tipo2_RelatorioT (Complete quarterly reports)
- **Institution Type**: 2 (Multiple Service Banks and Other Institutions)

**Raw Data Characteristics**:
- **Institution Coverage**: All supervised financial institutions
- **Report Categories**: 14+ financial report types
- **Data Points**: Financial statements, credit portfolios, market metrics
- **Format**: CSV with Brazilian number formatting (comma as decimal)

### 2. **Main Consolidated Database** 📚

**Primary Dataset**: `consolidated_cleaned.csv`

**Creation Process** (`etl.py`):
1. **Combination** (`combine_csv_files()`): Merges all raw quarterly files
2. **Transformation** (`transform_data()`): Cleans and standardizes data
3. **Institution Mapping**: Adds institution names from `consolidated_institutions.json`

**Schema Structure**:
```
- TipoInstituicao: Institution type code
- CodInst: 8-digit institution identifier (Primary Key)
- AnoMes: Date in YYYY-MM-DD format
- NumeroRelatorio: Report number (1-14+)
- NomeRelatorio: Report name/description
- Grupo: Group classification (or 'nagroup')
- Conta: Account code
- NomeColuna: Column/metric name
- DescricaoColuna: Column description
- Saldo: Financial value (standardized to float)
- NomeInstituicao: Institution name (from lookup)
- AnoMes_M: Monthly period
- AnoMes_Q: Quarterly period
- AnoMes_Y: Yearly period
- NomeRelatorio_Grupo_Coluna: Composite identifier
```

**Data Quality**:
- **Records**: ~1M+ consolidated records
- **Completeness**: High data quality with minimal missing values
- **Duplicates**: Removed during processing
- **Standardization**: Brazilian decimal format converted to float

### 3. **Specialized Transformed Datasets** 🎯

#### A. **Credit Portfolio Data**

**PF Credit** (`cred_pf.csv`):
- **Source**: Report 11 (Carteira de crédito ativa Pessoa Física)
- **Focus**: Individual person credit portfolios
- **Key Metrics**: Total PF portfolio, modalities breakdown

**PJ Credit** (`cred_pj.csv`):
- **Source**: Reports 13-14 (Carteira de crédito ativa Pessoa Jurídica)
- **Focus**: Legal entity credit portfolios
- **Segmentation**: Micro, Small, Medium, Large companies

**Combined Credit** (`credit_data.csv`):
- **Combination**: PF + PJ credit data
- **Usage**: Comprehensive credit analysis

#### B. **Market Analysis Data**

**Market Metrics** (`market_metrics.csv`):
- **Purpose**: Market share and competitive analysis
- **Key Metrics**:
  - Active client quantities
  - Credit portfolios (PF/PJ)
  - Financial intermediation revenues
  - Service revenues
  - Net profit
  - Deposits and funding

**Feature Mapping**:
```python
{
    'Quantidade de clientes com operações ativas': 'Client Market Share',
    'Carteira de Crédito Pessoa Física': 'PF Credit Portfolio',
    'Carteira de Crédito Pessoa Jurídica': 'PJ Credit Portfolio',
    'Lucro Líquido': 'Net Profit',
    'Captações': 'Funding/Deposits'
}
```

#### C. **Financial Performance Data**

**Financial Metrics** (`financial_metrics.csv`):
- **Source**: Reports 1 (Summary), 4 (P&L), 10 (Clients)
- **Calculated Metrics**:
  - **ROA**: Return on Assets
  - **ROE**: Return on Equity  
  - **Operating Revenue**: Aggregated from multiple revenue streams

**Processed Financial Metrics** (`financial_metrics_processed.csv`):
- **Advanced Processing**: Waterfall chart components
- **Three Value Types**:
  - **Absolute Values**: Raw financial amounts
  - **Percentage of Revenue**: Normalized to operating revenue
  - **Per Client Values**: Normalized to active client count

**Component Categories**:
- **Revenue Buildup**: Credit, TVM, Services, Fees
- **P&L Decomposition**: Revenue to Net Profit breakdown
- **Intermediation Breakdown**: Financial intermediation analysis

---

## 🔧 ETL Process Deep Dive

### **Step 1: Data Fetching** (`fetch_data.py`)

**Process**:
1. **API Integration**: Connects to BACEN IFDATA API
2. **Pagination Handling**: Downloads large datasets in chunks
3. **Error Handling**: Retry logic with exponential backoff
4. **Rate Limiting**: Respectful API usage with delays

**Institution Registry**:
- **Function**: `get_consolidated_institutions()`
- **Output**: `consolidated_institutions.json`
- **Deduplication**: Keeps most recent entry per institution

### **Step 2: Data Consolidation** (`etl.py`)

**Raw File Processing**:
```python
combine_csv_files() -> consolidated_reports.csv
```
- Combines 47+ quarterly files
- Removes duplicate rows
- Maintains data integrity

**Data Transformation**:
```python
transform_data() -> consolidated_cleaned.csv
```
- **Number Format**: Brazilian comma → decimal point
- **Date Processing**: YYYYMM → datetime with quarters
- **Institution Lookup**: Adds names via CodInst mapping
- **ID Standardization**: 8-digit zero-padded codes

### **Step 3: Specialized Dataset Creation**

**Credit Data Pipeline**:
```
consolidated_cleaned.csv → make_cred_pf_df() → cred_pf.csv
                        → make_cred_pj_df() → cred_pj.csv
                        → make_credit_data_df() → credit_data.csv
```

**Market Metrics Pipeline**:
```
consolidated_cleaned.csv → make_market_metrics_df() → market_metrics.csv
```

**Financial Metrics Pipeline**:
```
consolidated_cleaned.csv → make_financial_metrics_df() → financial_metrics.csv
                        → process_financial_metrics2() → financial_metrics_processed.csv
```

---

## 📊 Business Intelligence Layer

### **Report Types Available**

1. **Summary Reports** (Resumo)
   - Key financial ratios
   - Balance sheet summaries
   - Regulatory capital metrics

2. **Credit Portfolio Reports**
   - PF/PJ portfolio breakdown
   - Credit quality indicators
   - Sector concentration

3. **Income Statement Reports** (DRE)
   - Revenue decomposition
   - Cost structure analysis
   - Profitability metrics

4. **Market Analysis Reports**
   - Market share evolution
   - Competitive positioning
   - Client base analysis

### **Visualization Capabilities** (`plotting.py`)

**Market Share Analysis**:
- **Function**: `plot_market_share()`
- **Features**: Stacked area charts, top-N institutions
- **Metrics**: Any market metric with time series

**Credit Portfolio Analysis**:
- **Functions**: `plot_share_credit_modality()`, `plot_credit_portfolio()`
- **Features**: Modality breakdown, institution comparison
- **Views**: Absolute values or percentage shares

**Time Series Analysis**:
- **Function**: `plot_time_series()`
- **Features**: Multi-institution comparison
- **Value Types**: Absolute, % revenue, per-client

**Financial Waterfall Charts** (`plotting_financial_waterfall.py`):
- **Revenue Buildup**: How operating revenue is composed
- **P&L Decomposition**: From revenue to net profit
- **Intermediation Analysis**: Financial intermediation breakdown

---

## 🔑 Key Identifiers and Relationships

### **Primary Keys**
- **CodInst**: 8-digit institution code (unique identifier)
- **AnoMes**: Date reference (YYYY-MM-DD)
- **NumeroRelatorio**: Report type (1-14+)

### **Foreign Key Relationships**
```
consolidated_institutions.json (CodInst) ←→ consolidated_cleaned.csv (CodInst)
```

### **Categorical Classifications**

**Institution Types**:
- **Type 2**: Multiple Service Banks (primary focus)
- Includes: Commercial banks, cooperatives, investment banks

**Institution Segments**:
- **S1**: Large (≥10% market share)
- **S2**: Medium (0.1-10% market share)  
- **S3**: Small (<0.1% market share)
- **S4**: Credit cooperatives
- **S5**: Other institutions

**Control Types**:
- **Public**: Government-controlled
- **Private National**: Domestic private
- **Private Foreign**: Foreign-controlled

---

## 📈 Data Quality and Completeness

### **Coverage Statistics**
- **Time Period**: Q1 2013 - Q3 2024 (47 quarters)
- **Institutions**: 2,000+ financial institutions
- **Data Points**: 1M+ consolidated records
- **Reports**: 14+ quarterly report types

### **Data Quality Metrics**
- **Missing Values**: <5% across most datasets
- **Duplicates**: Removed during ETL process
- **Consistency**: Validated through cross-referencing
- **Accuracy**: Direct API source from BACEN

### **Update Frequency**
- **Quarterly Reports**: 45-60 days after quarter end
- **Revisions**: Possible for recent periods
- **Stability**: Final data after 6 months

---

## 🚀 Integration Points for v2.0

### **Database Design Recommendations**

**Primary Tables**:
1. **institutions** - Institution registry and metadata
2. **financial_reports** - Core financial data
3. **market_metrics** - Market analysis data
4. **credit_portfolios** - Credit-specific analysis

**Relationships**:
```sql
institutions (cod_inst) → financial_reports (cod_inst)
                      → market_metrics (cod_inst)
                      → credit_portfolios (cod_inst)
```

### **API Endpoint Mapping**

**Core Endpoints**:
- `/institutions` - Institution lookup and profiles
- `/market-share/{metric}` - Market share analysis
- `/credit-portfolio/{institution}` - Credit analysis
- `/financial-performance/{institution}` - Performance metrics
- `/time-series/{metric}` - Historical trends

### **Frontend Component Requirements**

**Dashboard Components**:
- Market share evolution charts
- Institution ranking tables
- Credit portfolio breakdowns
- Financial performance metrics
- Peer comparison tools

**Interactive Features**:
- Institution search and filtering
- Date range selection
- Metric comparison tools
- Export capabilities

---

## 🛠️ Technical Specifications

### **Data Processing Pipeline**

**Languages**: Python 3.8+
**Key Libraries**:
- `pandas`: Data manipulation and analysis
- `requests`: API integration
- `plotly`: Interactive visualizations
- `sqlite3`: Local database storage

**Performance Considerations**:
- **Memory Management**: Sample-based analysis for large files
- **Pagination**: API requests with chunking
- **Caching**: Institution registry cached locally
- **Batch Processing**: Quarterly data processed in batches

### **File Formats and Storage**

**Input Formats**:
- CSV (raw BACEN data)
- JSON (institution registry)

**Output Formats**:
- CSV (processed datasets)
- SQLite (optional local database)
- JSON (API responses)

**Storage Requirements**:
- **Raw Data**: ~500MB (47 quarterly files)
- **Processed Data**: ~200MB (consolidated datasets)
- **Total Storage**: ~1GB including backups

---

## 📋 Operational Procedures

### **Data Refresh Process**

1. **Quarterly Update**:
   ```bash
   python scripts/fetch_data.py  # New quarter data
   python scripts/etl.py         # Process new data
   ```

2. **Full Refresh**:
   ```bash
   python scripts/fetch_data.py  # All historical data
   python scripts/etl.py         # Full ETL pipeline
   ```

### **Quality Assurance Checks**

- **Data Validation**: Row counts and key metrics
- **Consistency Checks**: Cross-reference with previous periods
- **Business Logic**: Verify calculated ratios and aggregations

### **Monitoring and Alerting**

- **ETL Success/Failure**: Process completion status
- **Data Quality**: Missing data or anomaly detection
- **API Health**: BACEN API availability monitoring

---

## 🎯 Business Use Cases

### **Market Intelligence**
- **Market Share Trends**: Track institution positioning over time
- **Competitive Analysis**: Compare institutions within segments
- **New Entrant Tracking**: Monitor fintech and digital bank growth

### **Credit Risk Analysis**
- **Portfolio Concentration**: Analyze PF vs PJ exposure
- **Credit Quality Trends**: Monitor provisions and NPLs
- **Modality Analysis**: Understand credit product mix

### **Financial Performance**
- **Profitability Analysis**: ROE/ROA trends and peer comparison
- **Efficiency Metrics**: Cost-to-income ratios
- **Revenue Analysis**: Income composition and sustainability

### **Regulatory Compliance**
- **Basel Metrics**: Capital adequacy monitoring
- **Liquidity Indicators**: Funding stability analysis
- **Concentration Limits**: Portfolio and counterparty limits

---

## 📖 Glossary and Definitions

**BACEN**: Central Bank of Brazil (Banco Central do Brasil)
**IFDATA**: Selected Financial Institution Data API
**PF**: Pessoa Física (Individual Person)
**PJ**: Pessoa Jurídica (Legal Entity)
**DRE**: Demonstração de Resultado (Income Statement)
**TVM**: Títulos e Valores Mobiliários (Securities)
**CodInst**: Institution Code (8-digit identifier)

---

## ⚡ Quick Reference

### **Key Files Location**
```
data/
├── data_raw_reports/          # Raw quarterly files
├── consolidated_cleaned.csv   # Main database
├── market_metrics.csv         # Market analysis
├── financial_metrics.csv     # Financial performance
├── credit_data.csv           # Credit portfolios
└── consolidated_institutions.json  # Institution registry

scripts/
├── fetch_data.py             # Data fetching from API
├── etl.py                    # Data processing pipeline
├── plotting.py              # Visualization functions
└── plotting_financial_waterfall.py  # Advanced charts
```

### **Common Operations**
```python
# Load main dataset
df = pd.read_csv('data/consolidated_cleaned.csv')

# Get market share for a metric
from scripts.plotting import plot_market_share
fig = plot_market_share(df, feature='Lucro Líquido', top_n=10)

# Load financial metrics
fm = pd.read_csv('data/financial_metrics_processed.csv')
```

---

**Document Status**: Complete ✅  
**Next Update**: After Q4 2024 data release  
**Maintained By**: Banco Insights 2.0 Development Team