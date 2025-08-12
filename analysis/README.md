# 🔬 Analysis Hub - Banco Insights 2.0

This folder contains all analysis tools, scripts, and notebooks for data processing, validation, and metrics calculation.

---

## 📁 Structure Overview

```
analysis/
├── 📓 notebooks/          # Interactive Jupyter notebooks
│   ├── metrics_calculations_documentation.ipynb
│   ├── dashboard_charts_prototype.ipynb
│   └── data_validation_notebook.ipynb
│
└── 🐍 scripts/           # Python analysis scripts
    ├── data_transformation_scripts.py
    ├── market_analysis_documentation_supplement.py
    └── data_validation_script.py
```

---

## 📓 Notebooks

### **metrics_calculations_documentation.ipynb** ⭐
**Purpose**: Comprehensive documentation of all financial metrics calculations  
**Contains**:
- Balance sheet aggregations (Ativo_Total, Patrimonio_Liquido)
- Profitability ratios (ROE, ROA, NIM) with proper formulas
- Regulatory capital ratios (Basel, Tier1, CET1)
- Efficiency ratios (Cost/Income, Credit Loss)
- Statistical aggregations and market analysis

**Audience**: FSI professionals, quants, compliance teams

### **dashboard_charts_prototype.ipynb**
**Purpose**: Plotly chart prototypes and visualization examples  
**Contains**:
- Market share visualizations
- Credit portfolio breakdowns
- Time series trend analysis
- Interactive dashboard components

**Audience**: Frontend developers, UX designers

### **data_validation_notebook.ipynb**
**Purpose**: Data quality checks and validation procedures  
**Contains**:
- Balance sheet equation validation
- Cross-reference checks with BACEN data
- Outlier detection and data profiling
- Missing data analysis

**Audience**: Data engineers, QA teams

---

## 🐍 Scripts

### **data_transformation_scripts.py** ⭐
**Purpose**: Safe transformation from nested to transposed data format  
**Key Features**:
- Chunked processing to avoid memory issues with large CSV files
- Validation of metric identifiers against BACEN schema
- Generation of query-friendly tables with metrics as columns
- Sample data generation for testing

**Usage**:
```bash
python analysis/scripts/data_transformation_scripts.py
```

### **market_analysis_documentation_supplement.py**
**Purpose**: Customer market share analysis (focus on your key metric!)  
**Key Features**:
- `Quantidade_de_Clientes_com_Operacoes_Ativas` analysis
- Market concentration calculations (HHI)
- Business model classification (Mass Market vs Premium)
- Customer growth trend analysis

**Usage**:
```bash
python analysis/scripts/market_analysis_documentation_supplement.py
```

### **data_validation_script.py**
**Purpose**: Automated data quality checks  
**Key Features**:
- Database vs CSV comparison
- Metric value validation
- Data completeness reporting
- Automated quality scoring

---

## 🎯 Quick Start Guide

### **For Data Analysis**
1. Start with: `notebooks/data_validation_notebook.ipynb`
2. Review: `scripts/data_transformation_scripts.py`
3. Analyze: `notebooks/metrics_calculations_documentation.ipynb`

### **For Dashboard Development**
1. Explore: `notebooks/dashboard_charts_prototype.ipynb`
2. Run: `scripts/market_analysis_documentation_supplement.py`
3. Integrate: Chart components into frontend

### **For Quality Assurance**
1. Execute: `scripts/data_validation_script.py`
2. Review: `notebooks/data_validation_notebook.ipynb`
3. Validate: Results against `docs/analysis/CONFIDENCE_ASSESSMENT_REPORT.md`

---

## 🔧 Development Workflow

### **Adding New Analysis**
1. **Notebooks**: For exploratory analysis and documentation
2. **Scripts**: For reusable transformation and validation logic
3. **Documentation**: Update `docs/analysis/` with findings

### **Data Safety Guidelines**
- ⚠️ **NEVER** open `consolidated_cleaned.csv` directly (1GB+ file)
- ✅ **USE** chunked processing methods in scripts
- ✅ **VALIDATE** against sample data first
- ✅ **DOCUMENT** all calculations with audit trail

### **Testing New Metrics**
1. Add calculation logic to `metrics_calculations_documentation.ipynb`
2. Validate with sample data
3. Add to `data_transformation_scripts.py` for production
4. Update confidence assessment in docs

---

## 📊 Current Analysis Status

| Component | Status | Confidence | Notes |
|-----------|--------|------------|-------|
| **Data Transformation** | ✅ Complete | 9/10 | Excellent transposed design |
| **Customer Market Share** | ✅ Complete | 8/10 | Key metric well-implemented |
| **Financial Ratios** | ⚠️ Needs Fix | 4/10 | TTM methodology missing |
| **Regulatory Metrics** | ⚠️ Validation | 6/10 | Basel calculations need review |
| **Data Validation** | 🔄 In Progress | 3/10 | Critical ETL issues identified |

---

## 🚀 Next Steps

### **Priority 1 (Critical)**
- Fix ETL data loading issues causing 40-60% data loss
- Implement proper TTM calculations for ROE/ROA

### **Priority 2 (High)**
- Validate Basel ratio calculations against regulatory standards
- Enhance data validation framework with real-time monitoring

### **Priority 3 (Enhancement)**
- Add stress testing scenarios
- Implement advanced peer group analysis

---

**Navigation**: [← Back to Project Root](../README.md) | [View Documentation](../docs/) | [View Data Structure](../data_restructured/)