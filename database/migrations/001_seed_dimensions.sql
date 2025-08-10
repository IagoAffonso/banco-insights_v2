-- Seed Dimension Tables
-- Based on EDA analysis of BACEN data structure

-- =============================================
-- REPORT TYPES DIMENSION SEED
-- =============================================
-- Based on EDA analysis: 13 unique report types identified

INSERT INTO report_types (nome_relatorio, categoria, description) VALUES
('Resumo', 'Financial', 'Executive Summary - Key financial ratios and metrics'),
('Demonstração de Resultado', 'Financial', 'Income Statement (P&L) - Revenue and expense breakdown'),
('Ativo', 'Financial', 'Asset Structure - Asset composition and classification'),
('Passivo', 'Financial', 'Liability Structure - Liability composition and funding sources'),
('Carteira de crédito ativa - quantidade de clientes e de operações', 'Credit', 'Active client and operation counts'),
('Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento', 'Credit', 'Individual person credit by modality and maturity'),
('Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento', 'Credit', 'Legal entity credit by modality and maturity'),
('Carteira de crédito ativa Pessoa Jurídica - por porte do tomador', 'Credit', 'Legal entity credit by borrower size'),
('Carteira de crédito ativa Pessoa Jurídica - por atividade econômica (CNAE)', 'Credit', 'Legal entity credit by economic sector'),
('Carteira de crédito ativa - por indexador', 'Risk', 'Credit portfolio by interest rate indexer'),
('Carteira de crédito ativa - por nível de risco da operação', 'Risk', 'Credit portfolio by risk level (AA to H)'),
('Carteira de crédito ativa - por região geográfica', 'Risk', 'Credit portfolio by geographic region'),
('Informações de Capital', 'Capital', 'Capital adequacy and regulatory metrics');

-- =============================================
-- METRIC GROUPS DIMENSION SEED
-- =============================================
-- Based on EDA analysis: 54 unique groups identified

INSERT INTO metric_groups (grupo, categoria, description) VALUES
-- Default/Unclassified
('nagroup', 'Default', 'Default group for ungrouped metrics'),

-- Individual Person (PF) Credit Products
('Empréstimo com Consignação em Folha', 'Credit_PF', 'Payroll loans for individuals'),
('Empréstimo sem Consignação em Folha', 'Credit_PF', 'Non-payroll loans for individuals'),
('Veículos', 'Credit_PF', 'Vehicle financing for individuals'),
('Habitação', 'Credit_PF', 'Housing loans for individuals'),
('Cartão de Crédito', 'Credit_PF', 'Credit cards for individuals'),
('Rural e Agroindustrial', 'Credit_PF', 'Rural and agribusiness loans for individuals'),
('Outros Créditos', 'Credit_PF', 'Other credit products for individuals'),

-- Legal Entity (PJ) Credit Products  
('Operações com Recebíveis', 'Credit_PJ', 'Receivables operations for companies'),
('Capital de Giro', 'Credit_PJ', 'Working capital for companies'),
('Capital de Giro Rotativo', 'Credit_PJ', 'Revolving working capital for companies'),
('Investimento', 'Credit_PJ', 'Investment financing for companies'),
('Comércio Exterior', 'Credit_PJ', 'Foreign trade financing'),
('Habitacional', 'Credit_PJ', 'Housing for companies'),
('Cheque Especial e Conta Garantida', 'Credit_PJ', 'Overdraft facilities for companies'),

-- Economic Sectors (CNAE Classification)
('Indústrias de Transformação', 'Economic_Sector', 'Manufacturing industries'),
('Construção', 'Economic_Sector', 'Construction sector'),
('Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura', 'Economic_Sector', 'Agriculture, livestock, forestry, fishing and aquaculture'),
('Administração Pública, Defesa e Seguridade Social', 'Economic_Sector', 'Public administration, defense and social security'),
('Transporte, Armazenagem e Correio', 'Economic_Sector', 'Transport, storage and postal services'),
('Comércio, Reparação de Veículos Automotores e Motocicletas', 'Economic_Sector', 'Commerce and automotive repair'),
('Serviços Industriais de Utilidade Pública', 'Economic_Sector', 'Public utility services'),
('Industrias Extrativas', 'Economic_Sector', 'Extractive industries'),

-- Financial Statement Categories
('Resultado de Intermediação Financeira - Receitas de Intermediação Financeira', 'Income_Statement', 'Financial intermediation revenues'),
('Resultado de Intermediação Financeira - Despesas de Intermediação Financeira', 'Income_Statement', 'Financial intermediation expenses'),
('Outras Receitas/Despesas Operacionais', 'Income_Statement', 'Other operational revenues/expenses'),
('Captações - Depósito Total', 'Balance_Sheet', 'Total deposits'),
('Captações - Recursos de Aceites e Emissão de Títulos', 'Balance_Sheet', 'Acceptances and securities issuance'),

-- Regulatory Capital Categories
('Patrimônio de Referência para Comparação com o RWA', 'Regulatory_Capital', 'Reference equity for RWA comparison'),
('Ativos Ponderados pelo Risco (RWA)', 'Regulatory_Capital', 'Risk-weighted assets'),
('Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado', 'Regulatory_Capital', 'Market risk RWA'),

-- Company Size Categories
('Micro', 'Company_Size', 'Micro companies'),
('Pequena', 'Company_Size', 'Small companies'),
('Média', 'Company_Size', 'Medium companies'),
('Grande', 'Company_Size', 'Large companies'),

-- Geographic Regions
('Sudeste', 'Geographic', 'Southeast region'),
('Centro-oeste', 'Geographic', 'Center-west region'),
('Nordeste', 'Geographic', 'Northeast region'),
('Norte', 'Geographic', 'North region'),
('Sul', 'Geographic', 'South region'),
('Região não Informada', 'Geographic', 'Region not informed'),
('Total Exterior', 'Geographic', 'International total'),

-- Risk Levels
('AA', 'Risk_Level', 'Credit risk level AA (lowest risk)'),
('A', 'Risk_Level', 'Credit risk level A'),
('B', 'Risk_Level', 'Credit risk level B'),
('C', 'Risk_Level', 'Credit risk level C'),
('D', 'Risk_Level', 'Credit risk level D'),
('E', 'Risk_Level', 'Credit risk level E'),
('F', 'Risk_Level', 'Credit risk level F'),
('G', 'Risk_Level', 'Credit risk level G'),
('H', 'Risk_Level', 'Credit risk level H (highest risk)'),

-- Interest Rate Indexers
('Prefixado', 'Interest_Rate', 'Fixed rate'),
('CDI', 'Interest_Rate', 'CDI indexed'),
('SELIC', 'Interest_Rate', 'SELIC indexed'),
('IPCA', 'Interest_Rate', 'IPCA indexed'),
('IGPM', 'Interest_Rate', 'IGPM indexed'),
('TR/TBF', 'Interest_Rate', 'TR/TBF indexed'),
('TJLP', 'Interest_Rate', 'TJLP indexed'),
('TLP', 'Interest_Rate', 'TLP indexed');

-- =============================================
-- METRICS DIMENSION SEED
-- =============================================
-- Key metrics based on EDA analysis and frontend requirements

INSERT INTO metrics (nome_coluna, tipo_dado, unidade, description) VALUES
-- Asset Metrics
('Ativo Total', 'currency', 'R$ milhões', 'Total assets'),
('Disponibilidades', 'currency', 'R$ milhões', 'Cash and cash equivalents'),
('Operações de Crédito', 'currency', 'R$ milhões', 'Credit operations'),
('TVM e Instrumentos Financeiros Derivativos', 'currency', 'R$ milhões', 'Securities and financial derivatives'),

-- Credit Portfolio Metrics
('Total da Carteira de Pessoa Física', 'currency', 'R$ milhões', 'Total individual portfolio'),
('Total da Carteira de Pessoa Jurídica', 'currency', 'R$ milhões', 'Total corporate portfolio'),
('Quantidade de clientes com operações ativas', 'count', 'quantidade', 'Number of clients with active operations'),
('Quantidade de operações ativas', 'count', 'quantidade', 'Number of active operations'),

-- Maturity Bucket Metrics
('Vencido a Partir de 15 Dias', 'currency', 'R$ milhões', 'Past due 15+ days'),
('A Vencer em até 90 Dias', 'currency', 'R$ milhões', 'Maturing within 90 days'),
('A Vencer Entre 91 a 360 Dias', 'currency', 'R$ milhões', 'Maturing 91-360 days'),
('A Vencer Entre 361 a 1080 Dias', 'currency', 'R$ milhões', 'Maturing 361-1080 days'),
('A Vencer Entre 1081 a 1800 Dias', 'currency', 'R$ milhões', 'Maturing 1081-1800 days'),
('A Vencer Entre 1801 a 5400 Dias', 'currency', 'R$ milhões', 'Maturing 1801-5400 days'),
('A vencer Acima de 5400 Dias', 'currency', 'R$ milhões', 'Maturing over 5400 days'),

-- P&L Components
('Receitas de Intermediação Financeira', 'currency', 'R$ milhões', 'Financial intermediation revenues'),
('Despesas de Intermediação Financeira', 'currency', 'R$ milhões', 'Financial intermediation expenses'),
('Lucro Líquido', 'currency', 'R$ milhões', 'Net profit'),
('Rendas de Prestação de Serviços', 'currency', 'R$ milhões', 'Service fee income'),
('Despesas de Pessoal', 'currency', 'R$ milhões', 'Personnel expenses'),

-- Regulatory Metrics
('Índice de Basileia', 'ratio', '%', 'Basel ratio'),
('Índice de Imobilização', 'ratio', '%', 'Immobilization index'),
('Patrimônio de Referência', 'currency', 'R$ milhões', 'Regulatory capital'),
('RWA para Risco de Crédito', 'currency', 'R$ milhões', 'Credit risk RWA'),

-- Performance Ratios (calculated)
('ROE', 'ratio', '%', 'Return on Equity'),
('ROA', 'ratio', '%', 'Return on Assets'),
('Efficiency Ratio', 'ratio', '%', 'Operating efficiency ratio'),
('Capital Ratio', 'ratio', '%', 'Capital adequacy ratio'),
('NPL Ratio', 'ratio', '%', 'Non-performing loans ratio');

-- =============================================
-- SAMPLE INSTITUTIONS SEED
-- =============================================
-- Based on frontend mockData and major Brazilian banks

INSERT INTO institutions (cod_inst, cnpj, name, short_name, type, segment, control_type, region, city, founded_year, status) VALUES
('C0000001', '00.000.000/0001-91', 'Banco do Brasil S.A.', 'Banco do Brasil', 'Banco Múltiplo', 'S1', 'Público', 'DF', 'Brasília', 1808, 'active'),
('C0000341', '60.872.504/0001-23', 'Itaú Unibanco Holding S.A.', 'Itaú Unibanco', 'Banco Múltiplo', 'S1', 'Privado Nacional', 'SP', 'São Paulo', 1943, 'active'),
('C0000360', '00.360.305/0001-04', 'Caixa Econômica Federal', 'Caixa', 'Banco Múltiplo', 'S1', 'Público', 'DF', 'Brasília', 1861, 'active'),
('C0000237', '60.746.948/0001-12', 'Banco Bradesco S.A.', 'Bradesco', 'Banco Múltiplo', 'S1', 'Privado Nacional', 'SP', 'Osasco', 1943, 'active'),
('C0000033', '90.400.888/0001-42', 'Banco Santander (Brasil) S.A.', 'Santander Brasil', 'Banco Múltiplo', 'S1', 'Privado Estrangeiro', 'SP', 'São Paulo', 1982, 'active'),
('C0003967', '18.236.120/0001-58', 'Nu Pagamentos S.A.', 'Nubank', 'Banco Digital', 'S2', 'Privado Estrangeiro', 'SP', 'São Paulo', 2013, 'active'),
('C0004087', '04.902.979/0001-44', 'Banco Inter S.A.', 'Banco Inter', 'Banco Digital', 'S2', 'Privado Nacional', 'MG', 'Belo Horizonte', 1994, 'active'),
('C0001080', '02.398.976/0001-60', 'Banco BTG Pactual S.A.', 'BTG Pactual', 'Banco Múltiplo', 'S2', 'Privado Nacional', 'SP', 'São Paulo', 1983, 'active');

-- Update is_current flag for most recent quarter
UPDATE time_periods SET is_current = false;
UPDATE time_periods SET is_current = true WHERE year = 2024 AND quarter = 4;