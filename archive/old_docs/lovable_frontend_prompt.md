# 🏦 Banco Insights 2.0 - Complete Frontend Development Prompt for Lovable

## 📋 Project Overview

**Product**: Banco Insights 2.0 - Professional Banking Intelligence Platform
**Target Users**: Investment banking analysts, asset management research teams, financial professionals
**Data Source**: Brazilian Central Bank (BACEN) financial institution data
**Tech Stack**: React/Next.js, Tailwind CSS, Plotly.js for charts
**Design Goal**: Professional, clean, modern interface matching premium financial research tools

## 🎯 Core Value Proposition

Build a free, open-access, professional-grade platform for BACEN data insights and intelligence targeting investment banking & asset management research teams covering financial services in Brazil. The platform provides comprehensive analysis of 2,000+ Brazilian financial institutions with 743 unique metrics across 47 quarters (2013-2024).

## 🎨 Design System & Visual Identity

### **Color Palette**
- **Primary Navy**: #1e3a8a (deep professional blue)
- **Secondary Blue**: #3b82f6 (bright accent blue)
- **Success Green**: #10b981 (positive metrics)
- **Warning Amber**: #f59e0b (neutral alerts)
- **Error Red**: #ef4444 (negative metrics/alerts)
- **Cool Gray Scale**: #f8fafc, #e2e8f0, #64748b, #1e293b
- **Pure White**: #ffffff (backgrounds)

### **Typography**
- **Primary Font**: Inter (clean, professional, excellent for data)
- **Headers**: Font weights 600-700, sizes 24px-48px
- **Body Text**: Font weight 400-500, sizes 14px-16px
- **Data/Numbers**: Font weight 500-600, monospace for alignment
- **Captions**: Font weight 400, size 12px-14px

### **Design Principles**
-1. Clarity Over Clutter

Prioritize white space, alignment, and minimalism to reduce cognitive load. Every screen should feel calm, deliberate, and free of unnecessary decoration. Only show what’s essential at each moment. Use icons to help the user understand/navigate

2. Data as the Hero

Treat metrics, trends, and charts as primary content — not just accessories. Visualizations should be elegant, performant, and readable at a glance. Avoid dashboards that feel like spreadsheets; design for insight, not overwhelm.

3. Professional & Polished

Use a modern SaaS visual language: neutral backgrounds, tight typography, and purposeful color. The UI should evoke trust and precision, like tools used by analysts — but with the friendliness of consumer-grade software.

4. Accessible by Default

Design for everyone — high contrast, screen reader support, keyboard navigation, and strong visual hierarchy. Follow WCAG guidelines and structure content for users who may not be data experts, but rely on data to make decisions.

5. Responsive, Not Just Reactive

Optimized for desktop workflows, but thoughtfully adapted to tablets and mobile. Resize gracefully, maintain legibility and interaction patterns that respect device capabilities. No broken layouts — ever.

6. Quiet Confidence (Optional Add-on)

Visuals shouldn’t scream. Use color to guide, not distract. Animations, if any, should be subtle. The product should feel confident, fast, and reliable — like a premium tool that gets out of the user’s way.

- **Clean & Minimal**: Lots of white space, uncluttered layouts
- **Data-First**: Charts and metrics are the hero elements
- **Professional**: modern SaaS aesthetic
- **Accessible**: High contrast, clear hierarchy, keyboard navigation, Trust-building, user-friendly, “designed for non-technical teams”
- **Responsive**: Desktop-first but tablet/mobile friendly

## 📱 Page Structure & Navigation

### **Main Navigation (Header)**
```
[Banco Insights Logo] [Market Overview] [Institution Search] [Rankings] [Analysis Tools] [About] [Search Bar]
```

### **Key Pages to Build**

#### **1. Landing Page** (`/`)
- **Hero Section**:
  - Title: "Professional Banking Intelligence for Brazil"
  - Subtitle: "Free access to comprehensive BACEN data analysis covering 2,000+ financial institutions"
  - CTA Button: "Explore Market Data"
  - Background: Subtle gradient with abstract financial chart silhouette

- **Key Features Section** (3 columns):
  - "Market Share Analysis" - 743 unique metrics
  - "Institution Profiles" - Complete financial analysis
  - "Competitive Intelligence" - Peer benchmarking

- **Market Snapshot Section**:
  - 4 KPI cards: Total Market Assets, Number of Institutions, Latest Quarter, Data Coverage
  - Mini chart showing market concentration

- **Why Choose Banco Insights Section**:
  - Professional-grade analysis
  - Real BACEN regulatory data
  - Free and open access
  - Export capabilities

#### **2. Market Overview Dashboard** (`/market`)
- **Top Metrics Bar**: 6 KPI cards (Total Assets, Credit Portfolio, Market Leaders, etc.)
- **Market Share Chart Section**:
  - Large interactive area chart showing top 10 banks by assets
  - Metric selector dropdown (Total Assets, Credit Portfolio, Net Profit, etc.)
  - Time period selector (1Y, 2Y, 5Y, All Time)
- **Market Concentration Analysis**:
  - HHI index display
  - Top 5 vs Rest breakdown
  - Concentration trend mini-chart
- **Recent Highlights**:
  - Latest quarter key changes
  - New institution entries
  - Market trend indicators

#### **3. Institution Search Page** (`/institutions`)
- **Search Interface**:
  - Large search bar with autocomplete
  - Advanced filters sidebar: Institution Type, Size, Region, Control Type
  - Institution type badges (Commercial Banks, Cooperatives, etc.)
- **Search Results Grid**:
  - Institution cards with: Logo placeholder, Name, Key metrics, View Profile button
  - Sorting options: Assets, Alphabet, Market Share
  - Pagination with 20 results per page
- **Quick Access Section**:
  - "Top 20 by Assets" grid
  - "Recent Additions" list
  - "Most Searched" institutions

#### **4. Institution Profile Page** (`/institutions/[id]`)
- **Institution Header**:
  - Institution name, type, and regulatory code
  - Key metrics row: Total Assets, Credit Portfolio, ROE, Basel Ratio
  - Institution metadata: Founded, Headquarters, Control Type
- **Financial Performance Dashboard** (Grid Layout):
  - Balance Sheet Summary (pie chart of assets)
  - P&L Summary (waterfall chart of profit)
  - Key Ratios Table (ROE, ROA, Efficiency, etc.)
  - Credit Portfolio Breakdown (stacked bar chart)
- **Time Series Analysis**:
  - Interactive line chart with multiple metrics
  - Metric selector and time period controls
  - Growth rate indicators
- **Peer Comparison Section**:
  - Benchmarking table vs peer group
  - Ranking indicators
  - Percentile scores

#### **5. Rankings Page** (`/rankings`)
- **Rankings Dashboard**:
  - Metric selector dropdown (743 options)
  - Time period selector
  - Institution type filters
- **Rankings Table**:
  - Rank, Institution Name, Metric Value, Market Share, Change indicators
  - Sortable columns
  - Color-coded performance indicators
  - Export buttons
- **Visual Rankings**:
  - Horizontal bar chart of top 20
  - Interactive hover details
  - Comparison toggle

#### **6. Analysis Tools Page** (`/analysis`)
- **Tool Selection Grid** (2x2):
  - "Market Share Analysis" - Upload custom metrics
  - "Peer Benchmarking" - Compare institutions
  - "Time Series Analysis" - Trend analysis
  - "Credit Portfolio Analysis" - Detailed credit breakdown
- **Quick Analysis Section**:
  - Metric selector
  - Institution multi-select
  - Generate analysis button
- **Recent Analyses**:
  - Saved/bookmarked analysis list
  - Quick access buttons

## 📊 Chart Components & Data Visualization

### **Chart Types Required**
1. **Stacked Area Charts**: Market share evolution over time
2. **Line Charts**: Time series analysis, trend visualization
3. **Bar Charts**: Institution rankings, comparative metrics
4. **Pie/Donut Charts**: Portfolio breakdown, market concentration
5. **Waterfall Charts**: P&L decomposition, financial flow
6. **Scatter Plots**: Risk-return analysis, correlation
7. **Heat Maps**: Performance matrices, regional analysis

### **Chart Design Specifications**
- **Library**: Use Plotly.js for interactivity
- **Color Scheme**: Use defined brand colors consistently
- **Interactivity**: Hover tooltips, zoom/pan, crossfilter
- **Export**: PNG, SVG, PDF download options
- **Responsive**: Adapt to container sizes
- **Professional**: Clean axes, proper spacing, clear legends

### **Sample Chart Components Needed**

#### **Market Share Area Chart**
```javascript
// Stacked area chart showing market share evolution
// Top 10 institutions + "Others" category
// Interactive legend for show/hide
// Time period selector integration
// Hover showing exact values and percentages
```

#### **Institution Performance Dashboard Cards**
```javascript
// KPI Cards with:
// - Large metric value
// - Metric name and description
// - Period-over-period change (colored arrow)
// - Sparkline mini-chart
// - Percentile ranking vs peers
```

#### **Financial Metrics Comparison Table**
```javascript
// Sortable table with:
// - Institution names (linked to profiles)
// - Metric columns (configurable)
// - Color-coded performance indicators
// - Export functionality
// - Pagination for large datasets
```

## 🗂️ Mock Data Structure

### **Institution Data Sample**
```javascript
const mockInstitutions = [
  {
    id: "00360305",
    name: "CAIXA ECONOMICA FEDERAL",
    type: "Commercial Bank",
    control: "Public",
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
    lastUpdate: "2024-Q3"
  },
  // ... more institutions
];
```

### **Market Data Sample**
```javascript
const mockMarketData = [
  {
    quarter: "2024-Q3",
    metric: "Total Assets",
    institutions: [
      { name: "ITAU", value: 1823456789012, marketShare: 18.9 },
      { name: "BRADESCO", value: 1567890123456, marketShare: 16.2 },
      { name: "CAIXA", value: 1345678901234, marketShare: 13.9 },
      // ... more institutions
    ]
  }
];
```

### **Time Series Data Sample**
```javascript
const mockTimeSeries = [
  {
    institution: "ITAU",
    metric: "Total Assets",
    data: [
      { quarter: "2023-Q1", value: 1756789012345 },
      { quarter: "2023-Q2", value: 1778901234567 },
      { quarter: "2023-Q3", value: 1801234567890 },
      // ... more quarters
    ]
  }
];
```

## 🎛️ Interactive Components

### **Global Search Component**
```
[🔍] [Search institutions, metrics, or reports...] [Advanced Filters ⚙️]
```
- Autocomplete with institution names
- Search suggestions dropdown
- Recent searches
- Advanced filter modal

### **Metric Selector Component**
```
📊 Select Metric: [Total Assets ▼]
```
- Dropdown with 743+ available metrics
- Search within dropdown
- Categorized options (Assets, Credit, P&L, Ratios)
- Metric descriptions on hover

### **Time Period Selector**
```
📅 Period: [2024-Q3 ▼] to [2024-Q3 ▼] | [1Y] [2Y] [5Y] [All Time]
```
- Quarterly dropdown selectors
- Quick period buttons
- Custom range selection
- Period comparison toggle

### **Institution Multi-Select**
```
🏦 Compare: [ITAU ×] [BRADESCO ×] [+ Add Institution]
```
- Tag-style selected institutions
- Autocomplete add function
- Remove tags functionality
- Maximum selection limits

### **Export Options Component**
```
📥 Export: [PNG] [SVG] [PDF] [Excel] [📋 Copy Data]
```
- Multiple format options
- High-resolution downloads
- Data-only export options
- Copy to clipboard functionality

## 📋 Component Library Requirements

### **Layout Components**
- **Page Container**: Max-width container with proper spacing
- **Section Wrapper**: Consistent section spacing and backgrounds
- **Grid System**: Responsive grid layouts (2-col, 3-col, 4-col)
- **Card Component**: Standard card with shadow, padding, hover effects

### **Navigation Components**
- **Header Navigation**: Sticky header with logo and main nav
- **Breadcrumbs**: Page hierarchy navigation
- **Sidebar Navigation**: Collapsible sidebar for filters/tools
- **Tab Navigation**: Horizontal tabs for content switching

### **Data Display Components**
- **KPI Card**: Large metric display with change indicators
- **Data Table**: Sortable, filterable, paginated table
- **Metric Grid**: Grid layout for multiple metrics
- **Comparison Table**: Side-by-side institution comparison

### **Form Components**
- **Search Input**: Enhanced search with autocomplete
- **Select Dropdown**: Searchable dropdown with categories
- **Multi-Select**: Tag-based multi-selection
- **Date Range Picker**: Calendar-based date selection
- **Filter Panel**: Collapsible filter controls

### **Chart Container Components**
- **Chart Wrapper**: Responsive container for charts
- **Chart Controls**: Unified controls for chart interaction
- **Chart Export**: Export buttons and functionality
- **Chart Loading**: Loading states and error handling

## 🎯 User Experience Flow

### **Primary User Journey**
1. **Landing Page**: User understands value proposition
2. **Market Overview**: User explores market-wide trends
3. **Institution Search**: User finds specific institution
4. **Institution Profile**: User analyzes detailed metrics
5. **Analysis Tools**: User compares multiple institutions
6. **Export Results**: User exports data for research

### **Secondary User Flows**
- Quick market snapshot from landing page
- Direct institution lookup via search
- Rankings exploration for market leaders
- Analysis tool deep-dives

## 🔧 Technical Requirements

### **Performance Requirements**
- **Page Load Time**: <2 seconds initial load
- **Chart Rendering**: <1 second for complex charts
- **Search Responsiveness**: <300ms autocomplete
- **Mobile Performance**: Optimized for tablets

### **Browser Support**
- Chrome 90+ (primary)
- Firefox 88+
- Safari 14+
- Edge 90+

### **Responsive Breakpoints**
- Desktop: 1024px+ (primary focus)
- Tablet: 768px-1023px
- Mobile: 320px-767px (basic support)

### **Accessibility Requirements**
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader optimization
- High contrast mode support

## 📱 Mobile Considerations

### **Mobile Adaptations**
- **Simplified Navigation**: Hamburger menu
- **Stacked Layouts**: Single-column layouts on mobile
- **Touch-Friendly**: Larger touch targets (44px minimum)
- **Chart Adaptations**: Simplified mobile chart versions
- **Reduced Data**: Essential metrics only on small screens

### **Tablet Optimizations**
- **Two-Column Layouts**: Optimal use of tablet screen space
- **Chart Interactions**: Touch-friendly chart controls
- **Landscape/Portrait**: Adaptive layouts for orientation

## 🎨 Specific Design Elements

### **Logo & Branding**
- **Logo**: "Banco Insights" in Inter font, navy blue
- **Tagline**: "Professional Banking Intelligence"
- **Favicon**: "BI" monogram in brand colors

### **Button Styles**
- **Primary**: Navy background, white text, rounded corners
- **Secondary**: White background, navy border and text
- **Success**: Green background for positive actions
- **Outline**: Transparent background with colored border

### **Card Designs**
- **Standard Card**: White background, subtle shadow, 8px border radius
- **Metric Card**: Larger padding, accent border-left, hover lift effect
- **Institution Card**: Profile image placeholder, structured layout

### **Table Styles**
- **Header**: Gray background, bold text, sort indicators
- **Rows**: Alternating backgrounds, hover highlights
- **Borders**: Subtle gray borders, no heavy lines
- **Data Alignment**: Numbers right-aligned, text left-aligned

## 📊 Sample Content & Copy

### **Page Headlines**
- Landing: "Professional Banking Intelligence for Brazil"
- Market: "Brazilian Banking Market Overview"
- Institutions: "Search Financial Institutions"
- Profile: "[Institution Name] - Complete Analysis"
- Rankings: "Institution Rankings & Leaderboards"
- Analysis: "Advanced Analysis Tools"

### **Call-to-Action Copy**
- "Explore Market Data"
- "Search Institutions"
- "View Complete Profile"
- "Compare Institutions"
- "Generate Analysis"
- "Export Results"

### **Metric Descriptions**
- "Total Assets: Complete balance sheet assets including cash, securities, and credit portfolio"
- "Credit Portfolio: Active lending operations to individuals and corporations"
- "ROE: Return on Equity - profitability relative to shareholder equity"
- "Basel Ratio: Regulatory capital adequacy ratio per Basel requirements"

## ✅ Acceptance Criteria

### **Functional Requirements**
- [x] All 6 main pages implemented with proper routing
- [x] Responsive design working across all breakpoints
- [x] Interactive charts with Plotly.js integration
- [x] Search functionality with autocomplete
- [x] Data filtering and sorting capabilities
- [x] Export functionality (mock implementation)

### **Visual Requirements**
- [x] Consistent design system implementation
- [x] Professional financial services aesthetic
- [x] Clean, uncluttered layouts with proper spacing
- [x] Brand colors used consistently throughout
- [x] Typography hierarchy clear and readable

### **Performance Requirements**
- [x] Fast page navigation (<500ms)
- [x] Smooth chart interactions
- [x] Responsive layout adjustments
- [x] Optimized images and assets

### **User Experience Requirements**
- [x] Intuitive navigation flow
- [x] Clear information hierarchy
- [x] Consistent interaction patterns
- [x] Helpful micro-interactions and feedback

## 🚀 Delivery Expectations

### **File Structure**
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
├── data/ (mock data)
└── assets/
```

### **Key Files Expected**
- Complete React application with Next.js setup
- All 6 main pages implemented
- Component library with reusable components
- Mock data files with realistic sample data
- Responsive CSS with Tailwind
- Chart components with Plotly.js integration

### **Documentation Needed**
- README with setup instructions
- Component documentation
- Mock data structure explanation
- Design system guide

## 🎯 Success Metrics

### **Visual Quality**
- Professional appearance matching Bloomberg/Refinitiv standards
- Consistent brand implementation
- Clean, modern design aesthetic
- Proper use of white space and typography

### **Functionality**
- All interactive elements working properly
- Responsive behavior across devices
- Chart interactions smooth and intuitive
- Search and filtering working correctly

### **User Experience**
- Intuitive navigation flow
- Clear information hierarchy
- Fast and responsive interactions
- Professional feel suitable for financial analysts

---

**This prompt provides complete specifications for building a professional-grade static frontend for Banco Insights 2.0. The frontend should demonstrate the full potential of the platform with realistic mock data and professional design quality suitable for investment banking and asset management research teams.**
