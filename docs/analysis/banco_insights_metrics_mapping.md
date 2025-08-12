# 🎯 Banco Insights 2.0 - Complete Metrics Mapping

**Created**: January 2025  
**Purpose**: Comprehensive mapping of all metrics, views, and calculations needed for Banco Insights platform  
**Scope**: Dashboard requirements, API endpoints, and analytical capabilities

---

## 📊 Core Dashboard Requirements

Based on the Streamlit application structure, we need the following key views:

### **1. Market Share Analysis** 📊
*Source: `1_Market_Share_📊.py`*

#### Primary Metrics Needed:
```python
MARKET_SHARE_METRICS = {
    # Asset Metrics
    'Ativo_Total': 'Total market size and institution positioning',
    'Carteira_de_Credito_Classificada': 'Credit market share analysis',
    
    # Revenue Metrics  
    'Receitas_de_Intermediacao_Financeira': 'Financial intermediation revenue share',
    'Rendas_de_Prestacao_de_Servicos': 'Service fee market share',
    'Rendas_de_Tarifas_Bancarias': 'Banking fee market share',
    
    # Funding Metrics
    'Captacoes': 'Total funding market share',
    'Depositos_a_Vista': 'Demand deposit market share', 
    'Depositos_de_Poupanca': 'Savings deposit market share',
    'Depositos_a_Prazo': 'Time deposit market share',
    
    # Client Metrics
    'Quantidade_de_Clientes_com_Operacoes_Ativas': 'Active client market share',
    'Quantidade_de_Operacoes_Ativas': 'Active operations market share',
    
    # Profitability Metrics
    'Lucro_Liquido': 'Net profit market share'
}
```

#### Calculated Market Share Views:
```python
MARKET_CALCULATIONS = {
    'market_share_percentage': 'Institution_Value / Total_Market_Value * 100',
    'market_rank': 'Ranking by metric value (1 = largest)',
    'market_concentration_hhi': 'Herfindahl-Hirschman Index',
    'top_n_concentration': 'Top 5, 10, 20 institution concentration ratios',
    'market_growth_rate': 'QoQ and YoY market growth rates'
}
```

### **2. Credit Portfolio Analysis** 💰💳
*Source: `2_Share_por_Linha_Crédito💰.py`, `3_Carteira_Credito_IFs💳.py`*

#### Credit Modality Breakdown (PF - Pessoa Física):
```python
PF_CREDIT_MODALITIES = {
    'Emprestimo_com_Consignacao_em_Folha': 'Payroll loans',
    'Emprestimo_sem_Consignacao_em_Folha': 'Non-payroll loans', 
    'Veiculos': 'Vehicle financing',
    'Habitacao': 'Housing loans',
    'Cartao_de_Credito': 'Credit cards',
    'Rural_e_Agroindustrial': 'Rural/agribusiness',
    'Outros_Creditos': 'Other credits'
}
```

#### Credit Modality Breakdown (PJ - Pessoa Jurídica):
```python
PJ_CREDIT_MODALITIES = {
    'Capital_de_Giro': 'Working capital',
    'Capital_de_Giro_Rotativo': 'Revolving working capital',
    'Investimento': 'Investment financing', 
    'Operacoes_com_Recebiveis': 'Receivables operations',
    'Comercio_Exterior': 'Foreign trade financing',
    'Habitacional': 'Corporate housing loans',
    'Financiamento_de_Infraestrutura': 'Infrastructure financing',
    'Rural_e_Agroindustrial': 'Rural/agribusiness corporate',
    'Cheque_Especial_e_Conta_Garantida': 'Overdraft facilities'
}
```

#### Credit Risk Analysis:
```python
CREDIT_RISK_LEVELS = {
    'AA': 'Lowest risk (0-0.5% risk)',
    'A': 'Very low risk (0.5-1% risk)', 
    'B': 'Low risk (1-3% risk)',
    'C': 'Moderate risk (3-10% risk)',
    'D': 'High risk (10-30% risk)',
    'E': 'Very high risk (30-50% risk)',
    'F': 'Severe risk (50-70% risk)',
    'G': 'Critical risk (70-100% risk)', 
    'H': 'Loss (100% risk)'
}
```

#### Maturity Analysis:
```python
MATURITY_BUCKETS = {
    'Vencido_a_Partir_de_15_Dias': 'Past due 15+ days',
    'A_Vencer_em_ate_90_Dias': 'Maturing within 90 days',
    'A_Vencer_Entre_91_a_360_Dias': 'Maturing 91-360 days',
    'A_Vencer_Entre_361_a_1080_Dias': 'Maturing 361-1080 days', 
    'A_Vencer_Entre_1081_a_1800_Dias': 'Maturing 1081-1800 days',
    'A_Vencer_Entre_1801_a_5400_Dias': 'Maturing 1801-5400 days',
    'A_Vencer_Acima_de_5400_Dias': 'Maturing over 5400 days'
}
```

### **3. Income Statement Analysis** 📑
*Source: `4_DREs📑.py`*

#### Revenue Components:
```python
REVENUE_METRICS = {
    # Financial Intermediation Revenues
    'Receitas_de_Intermediacao_Financeira': 'Total financial intermediation revenue',
    'Rendas_de_Operacoes_de_Credito': 'Credit operation revenues',
    'Rendas_de_Operacoes_de_Arrendamento_Mercantil': 'Leasing operation revenues',
    'Rendas_de_Operacoes_com_TVM': 'Securities operation revenues',
    'Rendas_de_Operacoes_com_Instrumentos_Financeiros_Derivativos': 'Derivatives revenues',
    'Resultado_de_Operacoes_de_Cambio': 'FX operation results',
    'Rendas_de_Aplicacoes_Compulsorias': 'Required reserves revenues',
    
    # Other Operating Revenues
    'Rendas_de_Prestacao_de_Servicos': 'Service fee income',
    'Rendas_de_Tarifas_Bancarias': 'Banking fee income',
    'Outras_Receitas_Operacionais': 'Other operating revenues'
}
```

#### Expense Components:
```python
EXPENSE_METRICS = {
    # Financial Intermediation Expenses  
    'Despesas_de_Intermediacao_Financeira': 'Total financial intermediation expenses',
    'Despesas_de_Captacao': 'Funding costs',
    'Despesas_de_Obrigacoes_por_Emprestimos_e_Repasses': 'Loan/repo expenses',
    'Despesas_de_Operacoes_de_Arrendamento_Mercantil': 'Leasing operation expenses',
    'Resultado_de_Provisao_para_Creditos_de_Dificil_Liquidacao': 'Loan loss provisions',
    
    # Operating Expenses
    'Despesas_de_Pessoal': 'Personnel expenses',
    'Despesas_Administrativas': 'Administrative expenses', 
    'Despesas_Tributarias': 'Tax expenses',
    'Outras_Despesas_Operacionais': 'Other operating expenses'
}
```

#### P&L Calculated Metrics:
```python
PL_CALCULATIONS = {
    'Resultado_de_Intermediacao_Financeira': 'Financial intermediation net result',
    'Outras_Receitas_Despesas_Operacionais': 'Other operating net result',
    'Resultado_Operacional': 'Operating result',
    'Resultado_Nao_Operacional': 'Non-operating result',
    'Resultado_antes_da_Tributacao': 'Pre-tax result',
    'Lucro_Liquido': 'Net profit'
}
```

### **4. Time Series Analysis** 📈
*Source: `5_Series_Temporais_📈.py`*

#### Trend Analysis Metrics:
```python
TIME_SERIES_METRICS = {
    # Growth Rates
    'QoQ_Growth_Rate': 'Quarter-over-Quarter growth',
    'YoY_Growth_Rate': 'Year-over-Year growth', 
    'CAGR': 'Compound Annual Growth Rate',
    
    # Moving Averages
    'MA_4Q': '4-Quarter Moving Average',
    'MA_8Q': '8-Quarter Moving Average',
    
    # Volatility Measures
    'Standard_Deviation': 'Historical volatility',
    'Coefficient_of_Variation': 'Risk-adjusted variability',
    
    # Trend Indicators
    'Linear_Trend': 'Linear trend coefficient',
    'Seasonal_Component': 'Quarterly seasonal patterns'
}
```

### **5. Benchmarks and Peer Analysis** 🏗️
*Source: `99_Benchmarks_🏗️.py`*

#### Institution Segmentation:
```python
INSTITUTION_SEGMENTS = {
    'S1': 'Large banks (≥10% market share)',
    'S2': 'Medium banks (0.1-10% market share)', 
    'S3': 'Small banks (<0.1% market share)',
    'S4': 'Credit cooperatives',
    'S5': 'Other institutions'
}

CONTROL_TYPES = {
    'Public': 'Government-controlled institutions',
    'Private_National': 'Domestic private institutions',
    'Private_Foreign': 'Foreign-controlled institutions'  
}
```

#### Peer Comparison Metrics:
```python
PEER_BENCHMARKS = {
    # Performance Ratios
    'ROE': 'Return on Equity',
    'ROA': 'Return on Assets',  
    'Cost_Income_Ratio': 'Cost-to-Income ratio',
    'Net_Interest_Margin': 'Net interest margin',
    
    # Efficiency Ratios
    'Assets_per_Employee': 'Asset productivity',
    'Revenue_per_Client': 'Client monetization',
    'Cost_per_Client': 'Client acquisition/servicing cost',
    
    # Risk Metrics
    'Credit_Risk_Ratio': 'NPL to total credit ratio',
    'Provision_Coverage_Ratio': 'Provisions to NPL coverage',
    'Concentration_Risk': 'Portfolio concentration measures'
}
```

---

## 📈 Advanced Calculated Metrics

### **Financial Performance Ratios**

#### **Profitability Ratios:**
```python
PROFITABILITY_RATIOS = {
    'ROE': {
        'formula': 'Lucro_Liquido_TTM / Patrimonio_Liquido_Average * 100',
        'description': 'Return on Equity (annualized)',
        'interpretation': 'Higher values indicate better shareholder returns'
    },
    'ROA': {
        'formula': 'Lucro_Liquido_TTM / Ativo_Total_Average * 100',
        'description': 'Return on Assets (annualized)', 
        'interpretation': 'Efficiency of asset utilization for profit generation'
    },
    'Net_Interest_Margin': {
        'formula': '(Receitas_de_Intermediacao_Financeira - Despesas_de_Intermediacao_Financeira) / Ativo_Total_Average * 100',
        'description': 'Net interest margin',
        'interpretation': 'Core banking profitability measure'
    }
}
```

#### **Efficiency Ratios:**
```python
EFFICIENCY_RATIOS = {
    'Cost_Income_Ratio': {
        'formula': '(Despesas_de_Pessoal + Despesas_Administrativas) / (Receitas_de_Intermediacao_Financeira + Rendas_de_Prestacao_de_Servicos + Rendas_de_Tarifas_Bancarias) * 100',
        'description': 'Cost-to-Income ratio',
        'interpretation': 'Lower values indicate higher operational efficiency'
    },
    'Operating_Leverage': {
        'formula': '(Revenue_Growth_Rate - Cost_Growth_Rate)',
        'description': 'Operating leverage',
        'interpretation': 'Ability to grow revenue faster than costs'
    }
}
```

#### **Risk Metrics:**
```python
RISK_METRICS = {
    'Credit_Loss_Ratio': {
        'formula': 'Resultado_de_Provisao_para_Creditos_de_Dificil_Liquidacao / Carteira_de_Credito_Classificada * 100',
        'description': 'Credit loss provisions as % of credit portfolio',
        'interpretation': 'Higher values indicate higher credit risk'
    },
    'Basel_Capital_Ratio': {
        'formula': 'Patrimonio_de_Referencia / Ativos_Ponderados_pelo_Risco_RWA * 100',
        'description': 'Basel capital adequacy ratio',
        'interpretation': 'Regulatory capital strength (minimum 8%)'
    }
}
```

### **Market Analysis Calculations**

#### **Market Share and Concentration:**
```python
MARKET_CALCULATIONS = {
    'Market_Share': {
        'formula': 'Institution_Metric_Value / Sum_All_Institutions_Metric_Value * 100',
        'description': 'Institution market share percentage',
        'aggregations': ['sum', 'median', 'weighted_average']
    },
    'HHI_Index': {
        'formula': 'Sum(Market_Share_i^2) for all institutions i',
        'description': 'Herfindahl-Hirschman concentration index',
        'interpretation': 'HHI < 1500: competitive, 1500-2500: moderately concentrated, >2500: highly concentrated'
    },
    'CR_Ratios': {
        'formula': 'Sum of top N institution market shares',
        'variants': ['CR4', 'CR5', 'CR10', 'CR20'],
        'description': 'Concentration ratios for top N institutions'
    }
}
```

#### **Growth and Trend Analysis:**
```python
GROWTH_CALCULATIONS = {
    'QoQ_Growth': {
        'formula': '(Current_Quarter - Previous_Quarter) / Previous_Quarter * 100',
        'description': 'Quarter-over-Quarter growth rate'
    },
    'YoY_Growth': {
        'formula': '(Current_Quarter - Same_Quarter_Previous_Year) / Same_Quarter_Previous_Year * 100',
        'description': 'Year-over-Year growth rate'
    },
    'TTM_Growth': {
        'formula': '(Current_TTM - Previous_TTM) / Previous_TTM * 100',
        'description': 'Trailing Twelve Months growth rate'
    },
    'CAGR': {
        'formula': '(Ending_Value / Beginning_Value)^(1/number_of_years) - 1',
        'description': 'Compound Annual Growth Rate'
    }
}
```

---

## 🎯 Statistical Aggregation Requirements

### **Institution-Level Statistics** (for each metric):
```python
INSTITUTION_STATS = {
    'sum': 'Total value across all periods',
    'mean': 'Average value across periods',  
    'median': 'Median value across periods',
    'std': 'Standard deviation (volatility)',
    'min': 'Minimum historical value',
    'max': 'Maximum historical value',
    'q25': '25th percentile',  
    'q75': '75th percentile',
    'latest': 'Most recent quarter value',
    'yoy_growth': 'Year-over-year growth rate'
}
```

### **Market-Level Statistics** (across all institutions per period):
```python
MARKET_STATS = {
    'total_market': 'Sum across all institutions',
    'mean_institution': 'Average per institution',
    'median_institution': 'Median per institution',  
    'market_std': 'Cross-institutional standard deviation',
    'market_concentration': 'HHI concentration index',
    'market_growth': 'Total market growth rate',
    'institution_count': 'Number of active institutions'
}
```

### **Peer Group Statistics** (by segment/control type):
```python
PEER_GROUP_STATS = {
    'segment_total': 'Total within segment (S1, S2, etc.)',
    'segment_average': 'Average within segment',
    'segment_median': 'Median within segment',
    'segment_rank': 'Rank within segment',
    'percentile_rank': 'Percentile rank within segment'
}
```

---

## 📊 Dashboard Views and API Endpoints

### **Core API Endpoint Requirements:**

#### **Institution Profile API:**
```
GET /api/v1/institutions/{cod_inst}
GET /api/v1/institutions/{cod_inst}/summary?period={quarter}
GET /api/v1/institutions/{cod_inst}/performance?periods={quarters}
GET /api/v1/institutions/{cod_inst}/peer-comparison?segment={S1|S2|S3|S4|S5}
```

#### **Market Analysis API:**
```
GET /api/v1/market/overview?period={quarter}
GET /api/v1/market/share/{metric}?period={quarter}&top_n={10}
GET /api/v1/market/concentration?metric={metric}&period={quarter}
GET /api/v1/market/trends/{metric}?periods={quarters}
```

#### **Credit Portfolio API:**
```
GET /api/v1/credit/portfolio/{cod_inst}?period={quarter}
GET /api/v1/credit/modalities/{cod_inst}?type={PF|PJ}&period={quarter}
GET /api/v1/credit/risk-analysis/{cod_inst}?period={quarter}
GET /api/v1/credit/market-share?modality={modality}&period={quarter}
```

#### **Financial Performance API:**
```
GET /api/v1/financial/ratios/{cod_inst}?periods={quarters}
GET /api/v1/financial/pl-breakdown/{cod_inst}?period={quarter}
GET /api/v1/financial/efficiency/{cod_inst}?periods={quarters}
GET /api/v1/financial/benchmarks/{cod_inst}?segment={segment}
```

---

## 🔧 Implementation Priority

### **Phase 1 - Core Metrics (MVP)**
1. **Resumo Table**: Ativo_Total, Lucro_Liquido, Captacoes, Patrimonio_Liquido
2. **Market Share**: Basic market share calculations for key metrics  
3. **Growth Rates**: QoQ and YoY growth calculations
4. **Basic Ratios**: ROE, ROA, Basel ratio

### **Phase 2 - Credit Analysis** 
1. **Credit Tables**: All credit modality breakdowns
2. **Risk Analysis**: Credit risk level distributions
3. **Client Metrics**: Active clients and operations analysis

### **Phase 3 - Advanced Analytics**
1. **Performance Ratios**: Complete efficiency and profitability ratios
2. **Peer Benchmarking**: Segment-based peer group analysis  
3. **Trend Analysis**: Advanced time series and forecasting

### **Phase 4 - Market Intelligence**
1. **Concentration Analysis**: HHI and concentration ratios
2. **Competitive Positioning**: Market positioning analytics
3. **Scenario Analysis**: Stress testing and scenario modeling

---

**Status**: Comprehensive metrics mapping complete ✅  
**Next Steps**: Create Jupyter notebook with detailed calculation documentation