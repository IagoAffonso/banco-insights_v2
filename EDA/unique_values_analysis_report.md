# 📊 Unique Values Analysis Report - BACEN Data Schema

**Source**: `unique_values.json`  
**Purpose**: Comprehensive analysis of categorical variables in BACEN consolidated dataset  
**Date**: January 2025

---

## 📋 Executive Summary

This report analyzes the unique categorical values from the BACEN consolidated dataset, revealing the complete schema structure for Brazilian banking regulatory reports. The analysis covers **743 unique composite identifiers** across **4 main categorical dimensions**, providing deep insights into the data taxonomy and business logic.

---

## 🗂️ Data Schema Overview

### **Categorical Dimensions Analyzed**

| Dimension | Unique Values | Purpose |
|-----------|---------------|---------|
| **NomeRelatorio** | 13 types | Report categories |
| **Grupo** | 54 groups | Data grouping/classification |
| **NomeColuna** | 208 columns | Specific metrics/fields |
| **NomeRelatorio_Grupo_Coluna** | 743 identifiers | Composite unique identifiers |

---

## 📑 1. Report Types Analysis (`NomeRelatorio`)

### **Available Report Categories (13 types)**

#### **Core Financial Reports**
1. **"Resumo"** - Executive Summary
   - Key financial ratios and metrics
   - High-level institution overview

2. **"Demonstração de Resultado"** - Income Statement (P&L)
   - Revenue and expense breakdown
   - Profitability analysis

3. **"Ativo"** - Asset Structure
   - Asset composition and classification
   - Balance sheet assets

4. **"Passivo"** - Liability Structure
   - Liability composition
   - Funding sources analysis

#### **Credit Portfolio Reports**
5. **"Carteira de crédito ativa - quantidade de clientes e de operações"**
   - Active client and operation counts

6. **"Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento"**
   - Individual person credit by modality and maturity

7. **"Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento"**
   - Legal entity credit by modality and maturity

8. **"Carteira de crédito ativa Pessoa Jurídica - por porte do tomador"**
   - Legal entity credit by borrower size

9. **"Carteira de crédito ativa Pessoa Jurídica - por atividade econômica (CNAE)"**
   - Legal entity credit by economic sector

#### **Risk and Analytics Reports**
10. **"Carteira de crédito ativa - por indexador"**
    - Credit portfolio by interest rate indexer

11. **"Carteira de crédito ativa - por nível de risco da operação"**
    - Credit portfolio by risk level (AA to H)

12. **"Carteira de crédito ativa - por região geográfica"**
    - Credit portfolio by geographic region

13. **"Informações de Capital"**
    - Capital adequacy and regulatory metrics

---

## 🏷️ 2. Group Classifications Analysis (`Grupo`)

### **Primary Groups (54 total)**

#### **Default/Unclassified**
- **"nagroup"** - Default group for ungrouped metrics

#### **Credit Product Categories**
**Individual Person (PF) Products:**
- "Empréstimo com Consignação em Folha" (Payroll loans)
- "Empréstimo sem Consignação em Folha" (Non-payroll loans)
- "Veículos" (Vehicle financing)
- "Habitação" (Housing loans)
- "Cartão de Crédito" (Credit cards)
- "Rural e Agroindustrial" (Rural/agribusiness)
- "Outros Créditos" (Other credits)

**Legal Entity (PJ) Products:**
- "Operações com Recebíveis" (Receivables operations)
- "Capital de Giro" (Working capital)
- "Capital de Giro Rotativo" (Revolving working capital)
- "Investimento" (Investment financing)
- "Comércio Exterior" (Foreign trade)
- "Habitacional" (Housing for companies)
- "Cheque Especial e Conta Garantida" (Overdraft facilities)

#### **Economic Sectors (CNAE Classification)**
- "Indústrias de Transformação" (Manufacturing)
- "Construção" (Construction)
- "Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura" (Agriculture/livestock)
- "Administração Pública, Defesa e Seguridade Social" (Public administration)
- "Transporte, Armazenagem e Correio" (Transport/logistics)
- "Comércio, Reparação de Veículos Automotores e Motocicletas" (Commerce/automotive)
- "Serviços Industriais de Utilidade Pública" (Public utilities)
- "Industrias Extrativas" (Extractive industries)

#### **Financial Statement Categories**
- "Resultado de Intermediação Financeira - Receitas de Intermediação Financeira"
- "Resultado de Intermediação Financeira - Despesas de Intermediação Financeira"
- "Outras Receitas/Despesas Operacionais"
- "Captações - Depósito Total"
- "Captações - Recursos de Aceites e Emissão de Títulos"

#### **Regulatory Capital Categories**
- "Patrimônio de Referência para Comparação com o RWA"
- "Ativos Ponderados pelo Risco (RWA)"
- "Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado"

---

## 📊 3. Column Metrics Analysis (`NomeColuna`)

### **Key Metric Categories (208 total)**

#### **Asset Metrics**
- "Ativo Total" - Total assets
- "Disponibilidades" - Cash and equivalents
- "Operações de Crédito" - Credit operations
- "TVM e Instrumentos Financeiros Derivativos" - Securities and derivatives

#### **Credit Portfolio Metrics**
- "Total da Carteira de Pessoa Física" - Total individual portfolio
- "Total da Carteira de Pessoa Jurídica" - Total corporate portfolio
- "Quantidade de clientes com operações ativas" - Active client count
- "Quantidade de operações ativas" - Active operation count

#### **Maturity Buckets**
- "Vencido a Partir de 15 Dias" (Past due 15+ days)
- "A Vencer em até 90 Dias" (Maturing within 90 days)
- "A Vencer Entre 91 a 360 Dias" (91-360 days)
- "A Vencer Entre 361 a 1080 Dias" (361-1080 days)
- "A Vencer Entre 1081 a 1800 Dias" (1081-1800 days)
- "A Vencer Entre 1801 a 5400 Dias" (1801-5400 days)
- "A vencer Acima de 5400 Dias" (Over 5400 days)

#### **Risk Classifications**
- Credit risk levels: "AA", "A", "B", "C", "D", "E", "F", "G", "H"
- Company sizes: "Micro", "Pequena", "Média", "Grande"

#### **Geographic Regions**
- "Sudeste", "Centro-oeste", "Nordeste", "Norte", "Sul"
- "Região não Informada", "Total Exterior"

#### **Interest Rate Indexers**
- "Prefixado" (Fixed rate)
- "CDI", "SELIC", "IPCA", "IGPM", "TR/TBF", "TJLP", "TLP"
- "TCR pré", "TCR pós", "TRFC pós"
- "Libor", "Outras Taxas Pós-Fixadas"

#### **P&L Components**
- "Receitas de Intermediação Financeira" - Financial intermediation revenues
- "Despesas de Intermediação Financeira" - Financial intermediation expenses
- "Lucro Líquido" - Net profit
- "Rendas de Prestação de Serviços" - Service fee income
- "Despesas de Pessoal" - Personnel expenses

#### **Regulatory Metrics**
- "Índice de Basileia" - Basel ratio
- "Índice de Imobilização" - Immobilization index
- "Patrimônio de Referência" - Regulatory capital
- "RWA para Risco de Crédito" - Credit risk RWA

---

## 🔗 4. Composite Identifiers Analysis (`NomeRelatorio_Grupo_Coluna`)

### **Structure Pattern**
Format: `{ReportType}_{Group}_{Column}`

### **Key Insights from 743 Unique Identifiers**

#### **Most Complex Reports**
1. **Credit Portfolio Reports** - Highest granularity
   - PF modalities: 7 product types × 7 maturity buckets = 49+ combinations
   - PJ modalities: 11 product types × 7 maturity buckets = 77+ combinations
   - Economic sectors: 10 sectors × 7 maturity buckets = 70+ combinations

2. **Income Statement** - 27 unique line items
   - Revenue components (6 types)
   - Expense components (8 types)
   - Operating result calculations (13 types)

3. **Asset/Liability Structure** - 45+ line items each
   - Detailed breakdown by category and subcategory

#### **Business Logic Patterns**

**Hierarchical Structure:**
```
Report → Group → Specific Metric
├── Summary metrics (totals)
├── Detailed breakdowns
└── Risk/maturity analysis
```

**Calculation Dependencies:**
- Total fields aggregate sub-categories
- Ratios reference multiple base metrics
- Provisions offset gross values

---

## 💡 5. Business Intelligence Insights

### **Data Completeness Assessment**

#### **Comprehensive Coverage**
- **Time Series**: Quarterly data structure
- **Institution Coverage**: All supervised entities
- **Product Coverage**: Complete credit product spectrum
- **Risk Analysis**: Full risk spectrum (AA to H)
- **Geographic**: National coverage with regional breakdown

#### **Analytical Capabilities**

**Market Analysis:**
- Market share by any metric
- Competitive positioning
- Product penetration analysis

**Risk Management:**
- Credit quality trends
- Portfolio concentration
- Maturity mismatch analysis

**Performance Analysis:**
- Profitability decomposition
- Efficiency ratios
- Capital adequacy monitoring

### **Data Quality Indicators**

#### **Standardized Classifications**
- ✅ Consistent naming conventions
- ✅ Hierarchical group structure
- ✅ Standardized maturity buckets
- ✅ Regulatory compliance alignment

#### **Business Logic Validation**
- ✅ CNAE sector classifications
- ✅ Basel framework compliance
- ✅ Brazilian regulatory standards
- ✅ Complete P&L statement structure

---

## 🎯 6. Implementation Recommendations

### **Database Design**

#### **Primary Tables Structure**
```sql
-- Dimension Tables
institutions (cod_inst, nome_instituicao, tipo, segmento)
report_types (report_id, nome_relatorio, categoria)
metric_groups (group_id, grupo, categoria)
metrics (metric_id, nome_coluna, tipo_dado, unidade)

-- Fact Table
financial_data (
    cod_inst, 
    periodo, 
    report_id, 
    group_id, 
    metric_id, 
    valor
)
```

#### **Indexing Strategy**
- Composite indexes on (cod_inst, periodo, report_id)
- Group-specific indexes for performance
- Full-text search on metric names

### **API Endpoint Design**

#### **RESTful Structure**
```
/api/v1/institutions/{cod_inst}/reports/{report_type}
/api/v1/market-share/{metric}?period={YYYY-Q}
/api/v1/credit-portfolio/{institution}?modality={type}
/api/v1/risk-analysis/{metric}?risk_level={AA-H}
```

### **Frontend Component Mapping**

#### **Dashboard Widgets**
- **Summary Cards**: Key ratios from "Resumo" report
- **Credit Portfolio Charts**: PF/PJ breakdown visualizations
- **Risk Heatmaps**: Geographic and sector risk analysis
- **Time Series**: Trend analysis across quarters
- **Peer Comparison**: Institution benchmarking

---

## 📈 7. Data Modeling Opportunities

### **Calculated Metrics**

#### **Market Share Calculations**
```python
market_share = institution_value / total_market_value * 100
```

#### **Growth Rates**
```python
growth_rate = (current_value - previous_value) / previous_value * 100
```

#### **Risk-Adjusted Metrics**
```python
risk_adjusted_return = net_income / risk_weighted_assets
```

### **Aggregation Patterns**

#### **Time Series Aggregations**
- Quarterly to annual rollups
- Moving averages and trends
- Seasonal adjustments

#### **Hierarchical Aggregations**
- Product category to total portfolio
- Regional to national totals
- Individual to market aggregates

---

## ⚡ 8. Key Findings Summary

### **Data Richness**
- **743 unique metrics** provide comprehensive financial analysis capability
- **13 report types** cover all aspects of banking operations
- **54 group classifications** enable detailed segmentation
- **Complete regulatory coverage** aligns with Basel and BACEN requirements

### **Business Value**
- **Market Intelligence**: Complete competitive analysis capability
- **Risk Management**: Comprehensive risk assessment tools
- **Performance Monitoring**: Detailed profitability and efficiency tracking
- **Regulatory Compliance**: Full regulatory reporting alignment

### **Technical Implementation**
- **Standardized Schema**: Consistent structure enables automated processing
- **Scalable Design**: Hierarchical structure supports future expansion
- **Query Optimization**: Clear indexing strategy for performance
- **API Design**: RESTful structure for modern application integration

---

## 🔮 9. Future Enhancement Opportunities

### **Advanced Analytics**
- **Machine Learning**: Predictive modeling on financial metrics
- **Anomaly Detection**: Automated identification of unusual patterns
- **Clustering Analysis**: Institution similarity and segmentation
- **Stress Testing**: Scenario analysis capabilities

### **Data Enrichment**
- **Economic Indicators**: Macro-economic correlation analysis
- **External Data**: Credit bureau and market data integration
- **Real-time Updates**: Streaming data integration capabilities

---

**Document Status**: Complete Analysis ✅  
**Data Scope**: BACEN Consolidated Dataset - Complete Schema  
**Analysis Depth**: 743 Unique Identifiers Analyzed  
**Business Impact**: Comprehensive Banking Intelligence Platform Ready**