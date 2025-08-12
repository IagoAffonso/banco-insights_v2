# 🏦 Banco Insights 2.0 - Brazilian Banking Intelligence Platform

**Version**: 2.0  
**Last Updated**: January 2025  
**Status**: Development (Data Restructuring Phase Complete)

---

## 📋 Overview

Banco Insights 2.0 is a comprehensive Brazilian banking sector intelligence platform that analyzes data from 2,000+ financial institutions regulated by BACEN (Central Bank of Brazil). The platform processes quarterly reports from 2013-2024, providing market analysis, benchmarks, and financial insights.

**Key Innovation**: Transposed data structure design that transforms BACEN's nested format into query-friendly tables with metrics as direct columns.

---

## 📁 Project Structure

```
banco-insights-2.0/
├── 📄 README.md                    # This file - Project overview
├── 📄 CLAUDE.md                    # Development guidelines and instructions
│
├── 🗂️ docs/                        # Documentation Hub
│   ├── 📊 analysis/                # Analysis & QA Reports
│   │   ├── CONFIDENCE_ASSESSMENT_REPORT.md
│   │   ├── banco_insights_metrics_mapping.md
│   │   └── data_restructure_design.md
│   ├── 📋 planning/                # Planning & Strategy Documents
│   │   ├── DASHBOARD_DEVELOPMENT_PLAN.md
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── project-roadmap.md
│   │   └── feature_requirements_prioritization.md
│   └── 🛠️ technical/               # Technical Documentation
│       ├── Data Layer Report.md
│       ├── FRONTEND_BACKEND_MAPPING_REPORT.md
│       └── CODEBASE_SUMMARY.md
│
├── 🔬 analysis/                    # Analysis Tools & Scripts
│   ├── 📓 notebooks/              # Jupyter Notebooks
│   │   ├── metrics_calculations_documentation.ipynb
│   │   ├── dashboard_charts_prototype.ipynb
│   │   └── data_validation_notebook.ipynb
│   └── 🐍 scripts/                # Analysis Scripts
│       ├── data_transformation_scripts.py
│       ├── market_analysis_documentation_supplement.py
│       └── data_validation_script.py
│
├── 📊 data_restructured/           # NEW: Transposed Data Tables
│   ├── 📋 README.md               # Data structure documentation
│   ├── 🏛️ core_tables/            # Essential metrics (Resumo, Ativo, etc.)
│   ├── 💳 credit_tables/          # Credit portfolio analysis
│   ├── 📈 calculated_metrics/     # Derived ratios (ROE, ROA, etc.)
│   └── 🌐 market_analysis/        # Market-level aggregations
│
├── 🗃️ EDA/                        # Exploratory Data Analysis
│   ├── unique_values.json         # Complete data schema mapping
│   ├── banco_insights_knowledge_base.md
│   └── comprehensive_eda.ipynb
│
├── 🏗️ bacen_project_v1/           # Original V1.0 Application
│   ├── 🌐 streamlit_app/          # Current Streamlit frontend
│   ├── 🔌 api/                    # FastAPI backend
│   ├── 📊 data/                   # Raw BACEN data (consolidated_cleaned.csv)
│   ├── 🛠️ scripts/               # ETL and processing scripts
│   └── 📱 notebooks/              # Development notebooks
│
├── ⚛️ frontend/                   # Next.js Frontend (V2.0)
├── 🔧 backend/                    # Enhanced FastAPI Backend (V2.0)
├── 🗄️ database/                  # Database Schema & Migrations
│
├── ⚙️ config/                     # Configuration Files
│   └── dev.sh                     # Development scripts
│
└── 📦 archive/                    # Archived Files
    ├── 📄 old_docs/               # Deprecated documentation
    └── 🚀 deployment_configs/     # Old deployment configurations
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- PostgreSQL or Supabase account

### **V1.0 Streamlit Application (Current)**
```bash
# Navigate to V1 application
cd bacen_project_v1

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app/Intro.py

# Access at: http://localhost:8501
```

### **Data Analysis & Restructuring**
```bash
# Run data transformation (safe - uses chunked processing)
python analysis/scripts/data_transformation_scripts.py

# View restructured data
ls data_restructured/core_tables/

# Explore metrics documentation
jupyter notebook analysis/notebooks/metrics_calculations_documentation.ipynb
```

---

## 🎯 Key Features

### **✅ Completed (V1.0)**
- **Market Share Analysis**: Track institution positioning across 208+ metrics
- **Credit Portfolio Analysis**: PF/PJ breakdown by modality, risk, and region
- **Financial Performance**: P&L analysis and profitability ratios
- **Regulatory Metrics**: Basel ratios and capital adequacy monitoring
- **Time Series Analysis**: Historical trends and growth rates

### **🆕 V2.0 Innovations**
- **Transposed Data Structure**: Query-friendly format with metrics as columns
- **Customer Market Share**: Focus on `Quantidade_de_Clientes_com_Operacoes_Ativas`
- **Advanced Analytics**: Market concentration (HHI), peer benchmarking
- **Comprehensive QA**: FSI professional-grade validation framework
- **Modern Stack**: React frontend + Enhanced FastAPI backend

---

## 📊 Data Coverage

- **Time Period**: Q1 2013 - Q3 2024 (47+ quarters)
- **Institutions**: 2,000+ financial institutions
- **Data Points**: 1M+ consolidated records
- **Reports**: 13 report types, 208 unique metrics
- **Source**: BACEN IFDATA API (official regulatory data)

### **Key Metrics Available**
```python
# Balance Sheet
Ativo_Total, Patrimonio_Liquido, Carteira_de_Credito_Classificada

# P&L  
Lucro_Liquido, Receitas_de_Intermediacao_Financeira

# Regulatory
Indice_de_Basileia, Indice_de_Imobilizacao

# Market Share (Customer Focus)
Quantidade_de_Clientes_com_Operacoes_Ativas  # ⭐ Key metric
```

---

## 🔧 Development Workflow

### **Data Processing Pipeline**
1. **Raw Data**: BACEN IFDATA API → `bacen_project_v1/data/`
2. **ETL**: `scripts/etl.py` → `consolidated_cleaned.csv`
3. **Transformation**: `analysis/scripts/` → `data_restructured/`
4. **Analysis**: Jupyter notebooks for metrics validation
5. **Dashboard**: Streamlit (V1) / React (V2) frontends

### **Quality Assurance**
- **Data Validation**: Automated balance sheet equation checks
- **Calculation Audit**: FSI professional review simulation
- **Confidence Levels**: 1-10 scale for each metric category
- **Regulatory Compliance**: BACEN standards adherence

---

## 📈 Current Status & Next Steps

### **✅ Recently Completed**
- Complete data structure redesign (transposed format)
- Comprehensive metrics documentation with 95+ formulas
- QA review by simulated FSI professionals
- Customer market share analysis framework

### **⚠️ Priority Issues Identified**
1. **Critical**: ETL data loading issues (40-60% data loss)
2. **High**: ROE/ROA calculations missing TTM methodology
3. **Medium**: Basel ratio validation against regulatory standards

### **🎯 Next Phase (4-6 weeks)**
1. Fix ETL data integrity issues
2. Implement proper TTM calculations for financial ratios
3. Deploy V2.0 React frontend with transposed data structure
4. Production-ready deployment with full FSI approval

---

## 🤝 Contributing

### **Development Guidelines**
- Follow patterns in `CLAUDE.md` for development instructions
- Use safe data processing (chunked reading for large CSV files)
- Maintain comprehensive documentation for all calculations
- Include validation checks for new metrics

### **File Organization**
- **New analysis**: Add to `analysis/` folder
- **Documentation**: Use appropriate `docs/` subfolder
- **Data outputs**: Place in `data_restructured/`
- **Archive old files**: Move to `archive/` instead of deleting

---

## 📞 Support & Documentation

- **Development Guide**: `CLAUDE.md`
- **Metrics Documentation**: `analysis/notebooks/metrics_calculations_documentation.ipynb`
- **Data Structure**: `docs/analysis/data_restructure_design.md`
- **QA Report**: `docs/analysis/CONFIDENCE_ASSESSMENT_REPORT.md`
- **Technical Specs**: `docs/technical/`

---

## 📄 License

Proprietary - Brazilian Banking Intelligence Platform

---

**Last Updated**: January 2025  
**Maintained By**: Banco Insights Development Team  
**Status**: ✅ Data Restructuring Complete | 🔄 ETL Fixes In Progress