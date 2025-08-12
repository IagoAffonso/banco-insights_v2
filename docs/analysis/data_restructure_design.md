# 🏦 BACEN Data Restructure Design - Transposed Tables

**Created**: January 2025  
**Purpose**: Design document for restructuring consolidated_cleaned.csv into transposed, query-friendly format

---

## 🎯 Problem Statement

### Current Structure Issues
- **Nested Format**: Metrics stored as row identifiers (`NomeRelatorio_Grupo_Coluna`) rather than columns
- **Query Complexity**: To get "Ativo Total" for an institution, must filter by concatenated string
- **Analysis Difficulty**: No direct column access to key metrics like ROE, Basel Index
- **Database Inefficiency**: Star schema leads to complex joins and filters

### Current Data Shape (Long Format)
```
CodInst | AnoMes | NomeRelatorio_Grupo_Coluna | Saldo
12345   | 2024Q3 | Resumo_nagroup_Ativo Total | 1000000
12345   | 2024Q3 | Resumo_nagroup_Lucro Líquido | 50000
```

### Desired Data Shape (Wide Format)
```
CodInst | AnoMes | Ativo_Total | Lucro_Liquido | Basel_Index
12345   | 2024Q3 | 1000000     | 50000         | 12.5
```

---

## 🗂️ New Table Structure Design

### Table Organization by Report Type

Based on the unique values analysis, we'll create **13 separate CSV files** for each NomeRelatorio:

#### 1. **Resumo Table** (`resumo_quarterly.csv`)
**Purpose**: Executive summary with key ratios
```
Columns: CodInst, NomeInstituicao, AnoMes, AnoMes_Q, AnoMes_Y,
         Ativo_Total, Carteira_de_Credito_Classificada, 
         Passivo_Circulante_e_Exigivel_a_Longo_Prazo, Captacoes,
         Patrimonio_Liquido, Lucro_Liquido, Indice_de_Basileia,
         Indice_de_Imobilizacao
```

#### 2. **Ativo Table** (`ativo_quarterly.csv`)
**Purpose**: Balance sheet assets breakdown
```
Columns: CodInst, NomeInstituicao, AnoMes, AnoMes_Q, AnoMes_Y,
         Ativo_Total_Ajustado, Ativo_Total, Disponibilidades,
         Aplicacoes_Interfinanceiras_de_Liquidez,
         TVM_e_Instrumentos_Financeiros_Derivativos,
         Operacoes_de_Credito, Provisao_sobre_Operacoes_de_Credito,
         Operacoes_de_Credito_Liquidas_de_Provisao, [...]
```

#### 3. **Passivo Table** (`passivo_quarterly.csv`)
**Purpose**: Balance sheet liabilities breakdown
```
Columns: CodInst, NomeInstituicao, AnoMes, AnoMes_Q, AnoMes_Y,
         Depositos_a_Vista, Depositos_de_Poupanca, Depositos_a_Prazo,
         Obrigacoes_por_Operacoes_Compromissadas, Captacoes,
         Patrimonio_Liquido, Passivo_Total, [...]
```

#### 4. **DRE Table** (`demonstracao_resultado_quarterly.csv`)
**Purpose**: Income statement (P&L) analysis
```
Columns: CodInst, NomeInstituicao, AnoMes, AnoMes_Q, AnoMes_Y,
         Receitas_de_Intermediacao_Financeira,
         Rendas_de_Operacoes_de_Credito,
         Rendas_de_Operacoes_com_TVM,
         Despesas_de_Captacao, Despesas_de_Pessoal,
         Despesas_Administrativas, Lucro_Liquido, [...]
```

#### 5. **Capital Table** (`informacoes_capital_quarterly.csv`)
**Purpose**: Regulatory capital and Basel metrics
```
Columns: CodInst, NomeInstituicao, AnoMes, AnoMes_Q, AnoMes_Y,
         Capital_Principal_para_Comparacao_com_RWA,
         Patrimonio_de_Referencia_Nivel_I, Capital_Nivel_II,
         RWA_para_Risco_de_Credito, RWA_para_Risco_de_Mercado,
         Ativos_Ponderados_pelo_Risco_RWA,
         Indice_de_Capital_Principal, Indice_de_Basileia, [...]
```

#### 6-13. **Credit Portfolio Tables** (7 tables for different credit views)
- `credito_indexador_quarterly.csv` - Credit by interest rate indexer
- `credito_risco_quarterly.csv` - Credit by risk level (AA-H)  
- `credito_regiao_quarterly.csv` - Credit by geographic region
- `credito_pf_modalidade_quarterly.csv` - Individual credit by modality
- `credito_pj_modalidade_quarterly.csv` - Corporate credit by modality  
- `credito_pj_cnae_quarterly.csv` - Corporate credit by economic sector
- `credito_pj_porte_quarterly.csv` - Corporate credit by company size
- `credito_clientes_operacoes_quarterly.csv` - Client and operation counts

---

## 📊 Metrics Mapping and Calculations

### Direct Mapping (Simple Aggregations)
These metrics are direct sums or simple aggregations:

```python
DIRECT_METRICS = {
    'Ativo_Total': 'Resumo_nagroup_Ativo Total',
    'Carteira_de_Credito_Classificada': 'Resumo_nagroup_Carteira de Crédito Classificada',
    'Lucro_Liquido': 'Resumo_nagroup_Lucro Líquido',
    'Captacoes': 'Resumo_nagroup_Captações',
    'Patrimonio_Liquido': 'Resumo_nagroup_Patrimônio Líquido',
    'Indice_de_Basileia': 'Resumo_nagroup_Índice de Basileia',
    'Quantidade_de_Clientes_Ativos': 'Carteira de crédito ativa - quantidade de clientes e de operações_nagroup_Quantidade de clientes com operações ativas'
}
```

### Complex Calculated Metrics
These require calculations across multiple base metrics:

#### **Return on Equity (ROE)**
```python
ROE = (Lucro_Liquido_TTM / Patrimonio_Liquido_Average) * 100
```

#### **Return on Assets (ROA)** 
```python
ROA = (Lucro_Liquido_TTM / Ativo_Total_Average) * 100
```

#### **Basel Ratio (already calculated by BACEN)**
```python
Basel_Ratio = Patrimonio_de_Referencia / RWA_Total * 100
```

#### **Cost-to-Income Ratio**
```python
Cost_Income_Ratio = (Despesas_de_Pessoal + Despesas_Administrativas) / Receitas_de_Intermediacao_Financeira * 100
```

#### **Credit-to-Deposit Ratio**
```python
Credit_Deposit_Ratio = Carteira_de_Credito / Depositos_Total * 100
```

### Market-Level Aggregations
For market analysis, we need sector totals:

#### **Market Share Calculations**
```python
Market_Share_Asset = (Institution_Ativo_Total / Total_Market_Ativo_Total) * 100
Market_Share_Credit = (Institution_Credit / Total_Market_Credit) * 100
Market_Share_Deposits = (Institution_Deposits / Total_Market_Deposits) * 100
```

#### **Market Concentration (HHI)**
```python
HHI_Assets = sum(Market_Share_i^2) for all institutions
```

---

## 🛠️ Implementation Plan

### Phase 1: Core Tables Creation
1. **Resumo Table**: Essential metrics for dashboard
2. **DRE Table**: P&L analysis
3. **Capital Table**: Regulatory metrics

### Phase 2: Asset/Liability Tables  
1. **Ativo Table**: Balance sheet assets
2. **Passivo Table**: Balance sheet liabilities

### Phase 3: Credit Portfolio Tables
1. **Credit by Risk**: AA-H classifications
2. **Credit by Modality**: PF/PJ products
3. **Credit by Sector**: CNAE economic sectors

### Phase 4: Calculated Metrics Tables
1. **Market Share Table**: Institution vs market ratios
2. **Performance Ratios Table**: ROE, ROA, efficiency ratios
3. **Time Series Table**: Growth rates and trends

---

## 📈 Benefits of New Structure

### Query Performance
- **Direct Column Access**: `SELECT Ativo_Total FROM resumo_quarterly WHERE CodInst='12345'`
- **Simple Joins**: Easy to join tables by CodInst + AnoMes
- **Index Optimization**: Composite indexes on (CodInst, AnoMes)

### Analysis Simplicity
- **Pandas Friendly**: Direct column operations
- **SQL Friendly**: Standard WHERE clauses
- **BI Tool Compatible**: Works with Tableau, PowerBI, etc.

### Dashboard Development
- **React Components**: Easy to map API responses to chart data
- **Real-time Queries**: Fast aggregations and filtering
- **Comparison Views**: Institution vs peer group analysis

---

## 🔧 Column Naming Convention

### Standardization Rules
1. **Snake_Case**: All column names use underscores
2. **No Spaces**: Replace spaces with underscores
3. **No Special Characters**: Remove parentheses, dashes  
4. **Descriptive Names**: Keep business meaning clear
5. **Consistent Prefixes**: Group related metrics

### Examples
```python
COLUMN_MAPPING = {
    'Ativo Total': 'Ativo_Total',
    'Lucro Líquido': 'Lucro_Liquido',
    'Índice de Basileia': 'Indice_de_Basileia',
    'Receitas de Intermediação Financeira': 'Receitas_de_Intermediacao_Financeira',
    'A Vencer em até 90 Dias': 'A_Vencer_ate_90_Dias',
    'Quantidade de clientes com operações ativas': 'Quantidade_de_Clientes_com_Operacoes_Ativas'
}
```

---

## 📋 Data Quality Assurance

### Validation Rules
1. **Balance Sheet Validation**: Assets = Liabilities + Equity
2. **P&L Validation**: Revenue - Expenses = Net Income  
3. **Basel Validation**: Capital ratios within regulatory bounds
4. **Sum Checks**: Detail totals match summary figures

### Auditing Requirements
1. **Source Traceability**: Map each new column back to original identifier
2. **Calculation Documentation**: Document all derived metrics
3. **Data Lineage**: Track transformations from consolidated_cleaned.csv
4. **Quality Metrics**: Missing data rates, outlier detection

---

## 🎯 Success Metrics

### Performance Improvements
- **Query Time**: Reduce from seconds to milliseconds
- **Development Speed**: Faster dashboard development
- **Data Size**: Reduce redundancy in transposed format

### Business Impact
- **Ease of Use**: Non-technical users can query data
- **Analysis Speed**: Faster financial analysis workflows  
- **Reporting Accuracy**: Reduced calculation errors
- **Compliance**: Better regulatory reporting capabilities

---

**Next Steps**: 
1. Create folder structure for new CSV files
2. Develop Python transformation scripts  
3. Build metrics calculation documentation
4. Implement data validation framework