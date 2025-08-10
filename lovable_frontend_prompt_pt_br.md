# 🏦 Banco Insights 2.0 - Prompt Completo para Desenvolvimento Frontend (Lovable) - PT-BR

## 📋 Visão Geral do Projeto

**Produto**: Banco Insights 2.0 - Plataforma Profissional de Inteligência Bancária  
**Usuários-Alvo**: Analistas de investment banking, equipes de research de asset management, profissionais financeiros  
**Fonte de Dados**: Dados de instituições financeiras do Banco Central do Brasil (BACEN)  
**Tech Stack**: React/Next.js, Tailwind CSS, Plotly.js para gráficos  
**Objetivo de Design**: Interface profissional, limpa e moderna que rivaliza com ferramentas premium de research financeiro  

## 🎯 Proposta de Valor Central

Construir uma plataforma gratuita, de acesso aberto e de nível profissional para insights e inteligência de dados do BACEN, direcionada a equipes de investment banking e asset management research que cobrem serviços financeiros no Brasil. A plataforma oferece análise abrangente de 2.000+ instituições financeiras brasileiras com 743 métricas únicas ao longo de 47 trimestres (2013-2024).

## 🎨 Sistema de Design & Identidade Visual

### **Paleta de Cores**
- **Navy Primário**: #1e3a8a (azul profissional profundo)
- **Azul Secundário**: #3b82f6 (azul accent vibrante)  
- **Verde Sucesso**: #10b981 (métricas positivas)
- **Âmbar Aviso**: #f59e0b (alertas neutros)
- **Vermelho Erro**: #ef4444 (métricas/alertas negativos)
- **Escala Cinza Frio**: #f8fafc, #e2e8f0, #64748b, #1e293b
- **Branco Puro**: #ffffff (backgrounds)

### **Tipografia**
- **Fonte Primária**: Inter (limpa, profissional, excelente para dados)
- **Cabeçalhos**: Font weights 600-700, tamanhos 24px-48px
- **Texto Corpo**: Font weight 400-500, tamanhos 14px-16px
- **Dados/Números**: Font weight 500-600, monospace para alinhamento
- **Legendas**: Font weight 400, tamanho 12px-14px

### **Princípios de Design**
1. **Clareza sobre Desordem**
   - Priorizar espaço em branco, alinhamento e minimalismo para reduzir carga cognitiva. Cada tela deve parecer calma, deliberada e livre de decoração desnecessária. Mostrar apenas o essencial em cada momento. Usar ícones para ajudar o usuário a entender/navegar

2. **Dados como Protagonista**
   - Tratar métricas, tendências e gráficos como conteúdo primário — não apenas acessórios. Visualizações devem ser elegantes, performáticas e legíveis rapidamente. Evitar dashboards que pareçam planilhas; design para insights, não sobrecarga.

3. **Profissional & Polido**
   - Usar linguagem visual SaaS moderna: fundos neutros, tipografia precisa e cor proposital. A UI deve evocar confiança e precisão, como ferramentas usadas por analistas — mas com a amigabilidade de software consumer-grade.

4. **Acessível por Padrão**
   - Design para todos — alto contraste, suporte a leitor de tela, navegação por teclado e hierarquia visual forte. Seguir diretrizes WCAG e estruturar conteúdo para usuários que podem não ser especialistas em dados, mas dependem de dados para tomar decisões.

5. **Responsivo, Não Apenas Reativo**
   - Otimizado para workflows desktop, mas adaptado cuidadosamente para tablets e mobile. Redimensionar graciosamente, manter legibilidade e padrões de interação que respeitam capacidades do dispositivo. Sem layouts quebrados — nunca.

6. **Confiança Silenciosa**
   - Visuais não devem gritar. Usar cor para guiar, não distrair. Animações, se houver, devem ser sutis. O produto deve parecer confiante, rápido e confiável — como uma ferramenta premium que sai do caminho do usuário.

## 📱 Estrutura de Páginas & Navegação

### **Navegação Principal (Header)**
```
[Logo Banco Insights] [Visão Geral do Mercado] [Buscar Instituições] [Rankings] [Ferramentas de Análise] [Sobre] [Barra de Busca]
```

### **Páginas Principais a Construir**

#### **1. Landing Page** (`/`)
- **Seção Hero**:
  - Título: "Inteligência Bancária Profissional para o Brasil"
  - Subtítulo: "Acesso gratuito à análise abrangente de dados do BACEN cobrindo 2.000+ instituições financeiras"
  - Botão CTA: "Explorar Dados do Mercado"
  - Background: Gradiente sutil com silhueta abstrata de gráfico financeiro

- **Seção Principais Funcionalidades** (3 colunas):
  - "Análise de Market Share" - 743 métricas únicas
  - "Perfis de Instituições" - Análise financeira completa  
  - "Inteligência Competitiva" - Benchmarking entre pares

- **Seção Snapshot do Mercado**:
  - 4 cards de KPI: Ativos Totais do Mercado, Número de Instituições, Último Trimestre, Cobertura de Dados
  - Mini gráfico mostrando concentração do mercado
  
- **Seção Por Que Escolher o Banco Insights**:
  - Análise de nível profissional
  - Dados regulatórios reais do BACEN
  - Acesso gratuito e aberto
  - Capacidades de exportação

#### **2. Dashboard Visão Geral do Mercado** (`/market`)
- **Barra de Métricas Principais**: 6 cards de KPI (Ativos Totais, Carteira de Crédito, Líderes de Mercado, etc.)
- **Seção Gráfico de Market Share**:
  - Grande gráfico de área interativo mostrando top 10 bancos por ativos
  - Seletor dropdown de métrica (Ativos Totais, Carteira de Crédito, Lucro Líquido, etc.)
  - Seletor de período (1A, 2A, 5A, Todo Período)
- **Análise de Concentração do Mercado**:
  - Exibição do índice HHI
  - Breakdown Top 5 vs Resto
  - Mini-gráfico de tendência de concentração
- **Destaques Recentes**: 
  - Principais mudanças do último trimestre
  - Novas entradas de instituições
  - Indicadores de tendência do mercado

#### **3. Página de Busca de Instituições** (`/institutions`)
- **Interface de Busca**:
  - Grande barra de busca com autocomplete
  - Sidebar de filtros avançados: Tipo de Instituição, Tamanho, Região, Tipo de Controle
  - Badges de tipo de instituição (Bancos Comerciais, Cooperativas, etc.)
- **Grid de Resultados de Busca**:
  - Cards de instituição com: Placeholder de logo, Nome, Métricas principais, botão Ver Perfil
  - Opções de ordenação: Ativos, Alfabética, Market Share
  - Paginação com 20 resultados por página
- **Seção Acesso Rápido**:
  - Grid "Top 20 por Ativos"
  - Lista "Adições Recentes"
  - Instituições "Mais Buscadas"

#### **4. Página de Perfil da Instituição** (`/institutions/[id]`)
- **Cabeçalho da Instituição**:
  - Nome da instituição, tipo e código regulatório
  - Linha de métricas principais: Ativos Totais, Carteira de Crédito, ROE, Índice de Basileia
  - Metadados da instituição: Fundação, Sede, Tipo de Controle
- **Dashboard de Performance Financeira** (Layout Grid):
  - Resumo do Balanço (gráfico pizza de ativos)
  - Resumo DRE (gráfico waterfall de lucro)
  - Tabela de Índices Principais (ROE, ROA, Eficiência, etc.)
  - Breakdown da Carteira de Crédito (gráfico barras empilhadas)
- **Análise de Séries Temporais**:
  - Gráfico de linha interativo com múltiplas métricas
  - Seletor de métrica e controles de período
  - Indicadores de taxa de crescimento
- **Seção Comparação com Pares**:
  - Tabela de benchmarking vs grupo de pares
  - Indicadores de ranking
  - Scores de percentil

#### **5. Página de Rankings** (`/rankings`)
- **Dashboard de Rankings**:
  - Dropdown seletor de métrica (743 opções)
  - Seletor de período 
  - Filtros de tipo de instituição
- **Tabela de Rankings**:
  - Rank, Nome da Instituição, Valor da Métrica, Market Share, indicadores de Mudança
  - Colunas ordenáveis
  - Indicadores de performance com código de cores
  - Botões de exportação
- **Rankings Visuais**:
  - Gráfico de barras horizontal do top 20
  - Detalhes interativos no hover
  - Toggle de comparação

#### **6. Página de Ferramentas de Análise** (`/analysis`)
- **Grid de Seleção de Ferramentas** (2x2):
  - "Análise de Market Share" - Upload de métricas customizadas
  - "Benchmarking entre Pares" - Comparar instituições
  - "Análise de Séries Temporais" - Análise de tendências
  - "Análise de Carteira de Crédito" - Breakdown detalhado de crédito
- **Seção Análise Rápida**:
  - Seletor de métrica
  - Multi-seleção de instituição
  - Botão gerar análise
- **Análises Recentes**:
  - Lista de análises salvas/favoritadas
  - Botões de acesso rápido

## 📊 Componentes de Gráficos & Visualização de Dados

### **Tipos de Gráficos Necessários**
1. **Gráficos de Área Empilhada**: Evolução de market share ao longo do tempo
2. **Gráficos de Linha**: Análise de séries temporais, visualização de tendências
3. **Gráficos de Barras**: Rankings de instituições, métricas comparativas
4. **Gráficos Pizza/Donut**: Breakdown de portfólio, concentração de mercado
5. **Gráficos Waterfall**: Decomposição DRE, fluxo financeiro
6. **Gráficos de Dispersão**: Análise risco-retorno, correlação
7. **Mapas de Calor**: Matrizes de performance, análise regional

### **Especificações de Design de Gráficos**
- **Biblioteca**: Usar Plotly.js para interatividade
- **Esquema de Cores**: Usar cores da marca consistentemente
- **Interatividade**: Tooltips hover, zoom/pan, crossfilter
- **Exportação**: Opções de download PNG, SVG, PDF
- **Responsivo**: Adaptar a tamanhos de container
- **Profissional**: Eixos limpos, espaçamento adequado, legendas claras

### **Componentes de Gráfico Exemplo Necessários**

#### **Gráfico de Área Market Share**
```javascript
// Gráfico de área empilhada mostrando evolução de market share
// Top 10 instituições + categoria "Outros"
// Legenda interativa para mostrar/esconder
// Integração com seletor de período
// Hover mostrando valores exatos e percentuais
```

#### **Cards de Dashboard de Performance Institucional**
```javascript
// Cards de KPI com:
// - Valor grande da métrica
// - Nome e descrição da métrica  
// - Mudança período-sobre-período (seta colorida)
// - Mini-gráfico sparkline
// - Ranking percentil vs pares
```

#### **Tabela de Comparação de Métricas Financeiras**
```javascript
// Tabela ordenável com:
// - Nomes de instituições (linkados para perfis)
// - Colunas de métricas (configuráveis)
// - Indicadores de performance com código de cores
// - Funcionalidade de exportação
// - Paginação para datasets grandes
```

## 🗂️ Estrutura de Dados Mock

### **Amostra de Dados de Instituição**
```javascript
const mockInstitutions = [
  {
    id: "00360305",
    name: "CAIXA ECONOMICA FEDERAL",
    type: "Banco Comercial", 
    control: "Público",
    segment: "S1",
    totalAssets: 1547234567890,
    creditPortfolio: 892345678901,
    roe: 0.156,
    roa: 0.012,
    baselRatio: 0.165,
    marketShare: {
      assets: 15.2,
      credit: 18.7
    },
    lastUpdate: "2024-T3"
  },
  // ... mais instituições
];
```

### **Amostra de Dados de Mercado**  
```javascript
const mockMarketData = [
  {
    quarter: "2024-T3",
    metric: "Ativos Totais",
    institutions: [
      { name: "ITAU", value: 1823456789012, marketShare: 18.9 },
      { name: "BRADESCO", value: 1567890123456, marketShare: 16.2 },
      { name: "CAIXA", value: 1345678901234, marketShare: 13.9 },
      // ... mais instituições
    ]
  }
];
```

### **Amostra de Dados de Séries Temporais**
```javascript
const mockTimeSeries = [
  {
    institution: "ITAU",
    metric: "Ativos Totais", 
    data: [
      { quarter: "2023-T1", value: 1756789012345 },
      { quarter: "2023-T2", value: 1778901234567 },
      { quarter: "2023-T3", value: 1801234567890 },
      // ... mais trimestres
    ]
  }
];
```

## 🎛️ Componentes Interativos

### **Componente de Busca Global**
```
[🔍] [Buscar instituições, métricas ou relatórios...] [Filtros Avançados ⚙️]
```
- Autocomplete com nomes de instituições
- Dropdown de sugestões de busca
- Buscas recentes
- Modal de filtro avançado

### **Componente Seletor de Métrica**
```
📊 Selecionar Métrica: [Ativos Totais ▼]
```
- Dropdown com 743+ métricas disponíveis
- Busca dentro do dropdown
- Opções categorizadas (Ativos, Crédito, DRE, Índices)
- Descrições de métrica no hover

### **Seletor de Período**
```
📅 Período: [2024-T3 ▼] até [2024-T3 ▼] | [1A] [2A] [5A] [Todo Período]
```
- Seletores dropdown trimestrais
- Botões de período rápido
- Seleção de intervalo customizado
- Toggle de comparação de períodos

### **Multi-Seleção de Instituições**
```
🏦 Comparar: [ITAU ×] [BRADESCO ×] [+ Adicionar Instituição]
```
- Instituições selecionadas estilo tag
- Função de adicionar com autocomplete
- Funcionalidade de remover tags
- Limites máximos de seleção

### **Componente Opções de Exportação**
```
📥 Exportar: [PNG] [SVG] [PDF] [Excel] [📋 Copiar Dados]
```
- Opções de múltiplos formatos
- Downloads em alta resolução
- Opções de exportação apenas de dados
- Funcionalidade copiar para área de transferência

## 📋 Requisitos de Biblioteca de Componentes

### **Componentes de Layout**
- **Container de Página**: Container max-width com espaçamento adequado
- **Wrapper de Seção**: Espaçamento e backgrounds de seção consistentes
- **Sistema Grid**: Layouts grid responsivos (2-col, 3-col, 4-col)
- **Componente Card**: Card padrão com sombra, padding, efeitos hover

### **Componentes de Navegação**
- **Navegação Header**: Header sticky com logo e nav principal
- **Breadcrumbs**: Navegação de hierarquia de página
- **Navegação Sidebar**: Sidebar colapsível para filtros/ferramentas
- **Navegação Tab**: Tabs horizontais para switching de conteúdo

### **Componentes de Exibição de Dados**
- **Card KPI**: Exibição de métrica grande com indicadores de mudança
- **Tabela de Dados**: Tabela ordenável, filtrável, paginada
- **Grid de Métrica**: Layout grid para múltiplas métricas
- **Tabela de Comparação**: Comparação lado-a-lado de instituições

### **Componentes de Formulário**
- **Input de Busca**: Busca melhorada com autocomplete
- **Dropdown Select**: Dropdown pesquisável com categorias
- **Multi-Select**: Multi-seleção baseada em tags
- **Seletor de Intervalo de Data**: Seleção de data baseada em calendário
- **Painel de Filtro**: Controles de filtro colapsíveis

### **Componentes Container de Gráfico**
- **Wrapper de Gráfico**: Container responsivo para gráficos
- **Controles de Gráfico**: Controles unificados para interação com gráfico
- **Exportação de Gráfico**: Botões e funcionalidade de exportação
- **Loading de Gráfico**: Estados de loading e tratamento de erro

## 🎯 Fluxo de Experiência do Usuário

### **Jornada do Usuário Primário**
1. **Landing Page**: Usuário entende proposta de valor
2. **Visão Geral do Mercado**: Usuário explora tendências de mercado
3. **Busca de Instituição**: Usuário encontra instituição específica
4. **Perfil da Instituição**: Usuário analisa métricas detalhadas
5. **Ferramentas de Análise**: Usuário compara múltiplas instituições
6. **Exportar Resultados**: Usuário exporta dados para research

### **Fluxos de Usuário Secundários**
- Snapshot rápido do mercado pela landing page
- Busca direta de instituição via busca
- Exploração de rankings para líderes de mercado
- Deep-dives em ferramentas de análise

## 🔧 Requisitos Técnicos

### **Requisitos de Performance**
- **Tempo de Carregamento da Página**: <2 segundos carregamento inicial
- **Renderização de Gráfico**: <1 segundo para gráficos complexos
- **Responsividade da Busca**: <300ms autocomplete
- **Performance Mobile**: Otimizado para tablets

### **Suporte a Navegadores**
- Chrome 90+ (primário)
- Firefox 88+ 
- Safari 14+
- Edge 90+

### **Breakpoints Responsivos**
- Desktop: 1024px+ (foco primário)
- Tablet: 768px-1023px 
- Mobile: 320px-767px (suporte básico)

### **Requisitos de Acessibilidade**
- Conformidade WCAG 2.1 AA
- Suporte à navegação por teclado
- Otimização para leitor de tela
- Suporte a modo de alto contraste

## 📱 Considerações Mobile

### **Adaptações Mobile**
- **Navegação Simplificada**: Menu hamburger
- **Layouts Empilhados**: Layouts single-column no mobile
- **Touch-Friendly**: Alvos de toque maiores (mínimo 44px)
- **Adaptações de Gráfico**: Versões simplificadas de gráfico para mobile
- **Dados Reduzidos**: Apenas métricas essenciais em telas pequenas

### **Otimizações Tablet**
- **Layouts Duas Colunas**: Uso otimizado do espaço da tela do tablet
- **Interações de Gráfico**: Controles de gráfico touch-friendly
- **Paisagem/Retrato**: Layouts adaptativos para orientação

## 🎨 Elementos de Design Específicos

### **Logo & Branding**
- **Logo**: "Banco Insights" em fonte Inter, azul navy
- **Tagline**: "Inteligência Bancária Profissional" 
- **Favicon**: Monograma "BI" nas cores da marca

### **Estilos de Botão**
- **Primário**: Background navy, texto branco, cantos arredondados
- **Secundário**: Background branco, borda e texto navy
- **Sucesso**: Background verde para ações positivas
- **Outline**: Background transparente com borda colorida

### **Designs de Card**
- **Card Padrão**: Background branco, sombra sutil, border radius 8px
- **Card de Métrica**: Padding maior, border-left accent, efeito hover lift
- **Card de Instituição**: Placeholder de imagem de perfil, layout estruturado

### **Estilos de Tabela**
- **Header**: Background cinza, texto bold, indicadores de ordenação
- **Linhas**: Backgrounds alternados, destaques hover
- **Bordas**: Bordas cinza sutis, sem linhas pesadas
- **Alinhamento de Dados**: Números alinhados à direita, texto à esquerda

## 📊 Conteúdo e Copy de Exemplo

### **Headlines de Página**
- Landing: "Inteligência Bancária Profissional para o Brasil"
- Mercado: "Visão Geral do Mercado Bancário Brasileiro"
- Instituições: "Buscar Instituições Financeiras"
- Perfil: "[Nome da Instituição] - Análise Completa"
- Rankings: "Rankings e Leaderboards de Instituições"
- Análise: "Ferramentas de Análise Avançada"

### **Copy de Call-to-Action**
- "Explorar Dados do Mercado"
- "Buscar Instituições"
- "Ver Perfil Completo"
- "Comparar Instituições"
- "Gerar Análise"
- "Exportar Resultados"

### **Descrições de Métricas**
- "Ativos Totais: Ativos completos do balanço incluindo caixa, títulos e carteira de crédito"
- "Carteira de Crédito: Operações de empréstimo ativas para pessoas físicas e jurídicas"
- "ROE: Retorno sobre Patrimônio Líquido - rentabilidade relativa ao patrimônio dos acionistas"
- "Índice de Basileia: Índice de adequação de capital regulatório conforme requisitos de Basileia"

## ✅ Critérios de Aceitação

### **Requisitos Funcionais**
- [x] Todas as 6 páginas principais implementadas com roteamento adequado
- [x] Design responsivo funcionando em todos os breakpoints
- [x] Gráficos interativos com integração Plotly.js
- [x] Funcionalidade de busca com autocomplete
- [x] Capacidades de filtragem e ordenação de dados
- [x] Funcionalidade de exportação (implementação mock)

### **Requisitos Visuais**
- [x] Implementação consistente do sistema de design
- [x] Estética profissional de serviços financeiros
- [x] Layouts limpos e desorganizados com espaçamento adequado
- [x] Cores da marca usadas consistentemente
- [x] Hierarquia tipográfica clara e legível

### **Requisitos de Performance**
- [x] Navegação rápida entre páginas (<500ms)
- [x] Interações suaves de gráfico
- [x] Ajustes responsivos de layout
- [x] Imagens e assets otimizados

### **Requisitos de Experiência do Usuário**
- [x] Fluxo de navegação intuitivo
- [x] Hierarquia de informação clara
- [x] Padrões de interação consistentes
- [x] Micro-interações úteis e feedback

## 🚀 Expectativas de Entrega

### **Estrutura de Arquivos**
```
src/
├── components/
│   ├── layout/
│   ├── charts/
│   ├── forms/
│   └── ui/
├── pages/
├── styles/
├── utils/
├── data/ (dados mock)
└── assets/
```

### **Arquivos-Chave Esperados**
- Aplicação React completa com setup Next.js
- Todas as 6 páginas principais implementadas
- Biblioteca de componentes com componentes reutilizáveis
- Arquivos de dados mock com dados de amostra realistas
- CSS responsivo com Tailwind
- Componentes de gráfico com integração Plotly.js

### **Documentação Necessária**
- README com instruções de setup
- Documentação de componentes
- Explicação da estrutura de dados mock
- Guia do sistema de design

## 🎯 Métricas de Sucesso

### **Qualidade Visual**
- Aparência profissional compatível com padrões Bloomberg/Refinitiv
- Implementação consistente da marca
- Estética de design limpa e moderna
- Uso adequado de espaço em branco e tipografia

### **Funcionalidade**
- Todos os elementos interativos funcionando adequadamente
- Comportamento responsivo em dispositivos
- Interações de gráfico suaves e intuitivas
- Busca e filtragem funcionando corretamente

### **Experiência do Usuário**
- Fluxo de navegação intuitivo
- Hierarquia de informação clara
- Interações rápidas e responsivas
- Sensação profissional adequada para analistas financeiros

---

**Este prompt fornece especificações completas para construir um frontend estático de nível profissional para o Banco Insights 2.0. O frontend deve demonstrar todo o potencial da plataforma com dados mock realistas e qualidade de design profissional adequada para equipes de investment banking e asset management research.**