# Banco Insights 2.0 - Dashboard Development Plan

## Executive Summary

This document outlines the comprehensive plan for developing interactive dashboards and visualizations for Banco Insights 2.0, based on strategic analysis from FSI product expertise, UX design best practices, and technical visualization architecture. The plan prioritizes the most impactful features for Brazilian banking sector analysis targeting investment banking and asset management professionals.

## Current State Analysis (v1.0)

### Existing Features
- **Market Share Analysis**: Institution-level and metric-based market share tracking
- **Credit Portfolio Analysis**: PF/PJ breakdown across 19 credit modalities  
- **Financial Statements (DRE)**: Income statement analysis with multiple normalization methods
- **Time Series Comparisons**: Multi-institution metric tracking across 12+ years
- **Coverage**: 2,000+ BACEN-regulated institutions with quarterly data (2013-2024)

### Current UX Patterns
- Single chart per page via Streamlit
- Basic sidebar controls (dropdowns, date selectors)
- Simple navigation between analysis types
- Limited interactivity and drill-down capabilities

## Strategic Dashboard Requirements

### TIER 1: High Impact - Immediate Development Priority

#### 1. Risk & Credit Quality Dashboard 🚨
**Business Value**: Critical for credit analysts and investment risk assessment

**Core Features**:
- NPL evolution by institution and credit segment
- Provisioning ratios and coverage analysis  
- Credit concentration metrics (HHI, top exposures)
- Vintage analysis for credit performance
- Recovery rate benchmarking

**Key Metrics**: NPL ratios, provision/credit ratios, charge-off rates, recovery rates, concentration indices

**Interactive Parameters**:
- Risk rating segments (AA to H)
- Geographic concentration filters
- Industry sector breakdowns
- Vintage cohort selection

#### 2. Profitability & Efficiency Benchmarking Dashboard 📈
**Business Value**: Essential for equity analysts and investment managers evaluating operational performance

**Core Features**:
- ROE/ROA decomposition (DuPont analysis)
- Cost-to-income ratio evolution
- Net interest margin analysis
- Fee income efficiency metrics
- Productivity ratios (revenue/FTE, assets/FTE)

**Key Metrics**: ROE, ROA, Cost/Income, NIM, Operating leverage, Efficiency ratios

**Interactive Parameters**:
- Peer group selection (by asset size, business model)
- Efficiency frontier analysis
- Cost component breakdown
- Revenue mix analysis

#### 3. Capital & Regulatory Compliance Dashboard 🛡️
**Business Value**: Critical for understanding regulatory strength and growth capacity

**Core Features**:
- Basel III capital ratios evolution
- Tier 1/Tier 2 capital composition
- Regulatory capital vs. market cap analysis
- Stress testing implications
- Leverage ratio tracking

**Key Metrics**: CET1 ratio, Tier 1 capital, CAR, Leverage ratio, RWA

**Interactive Parameters**:
- Capital adequacy thresholds
- Risk-weighted asset breakdowns
- Regulatory buffer analysis
- Capital distribution capacity

### TIER 2: Medium Impact - Follow-On Development

#### 4. Market Positioning & Competitive Intelligence Dashboard
- Market share momentum analysis
- Competitive response tracking
- Product penetration rates
- Geographic market presence mapping

#### 5. Sectoral & Economic Sensitivity Dashboard  
- Credit exposure by economic sector
- Interest rate sensitivity analysis
- Economic cycle correlation metrics
- Regional economic exposure

#### 6. Digital Banking & Innovation Dashboard
- Digital channel adoption rates
- Mobile/online transaction volumes
- Digital product penetration
- Technology investment tracking

## UX/UI Architecture Design

### Dashboard Layout System

#### Multi-Chart Grid Architecture
Replace single-chart pages with dashboard grids containing multiple related visualizations:

```
┌─────────────────┬─────────────────┬─────────────────┐
│   Primary KPI   │  Secondary KPI  │  Tertiary KPI   │
│    (Large)      │    (Medium)     │    (Small)      │
├─────────────────┴─────────────────┼─────────────────┤
│        Main Analysis Chart        │  Supporting     │
│         (Timeline/Waterfall)      │   Metrics       │
├───────────────────────────────────┼─────────────────┤
│          Secondary Chart          │  Benchmarking   │
│        (Comparative Analysis)     │    Rankings     │
└───────────────────────────────────┴─────────────────┘
```

### Interactive Control Patterns

#### Advanced Filter Panel
- **Institution Selector**: Multi-tier with categories (Tier 1, Tier 2, Fintech, Cooperative)
- **Smart Date Range**: Quarterly presets with comparative analysis options
- **Metric Parameters**: Value types, benchmarking options, currency adjustments
- **Preset Configurations**: Save and load common analysis setups

#### Progressive Disclosure Drill-Down
- **Level 1**: Dashboard overview with key metrics
- **Level 2**: Click chart sections to drill into sub-categories  
- **Level 3**: Institution-specific detailed analysis
- **Level 4**: Historical trend analysis with peer comparisons

### Visual Design Standards

#### Financial Color Palette
- **Positive Performance**: Green (#16a34a)
- **Negative Performance**: Red (#dc2626)  
- **Neutral/Stable**: Gray (#64748b)
- **Warning Indicators**: Amber (#f59e0b)
- **Benchmark Lines**: Blue (#3b82f6)

#### Institution Tier Colors
- **Tier 1 Banks**: Navy Blue (#1e40af)
- **Tier 2 Banks**: Purple (#7c3aed)
- **Fintech/Digital**: Green (#059669)
- **Cooperatives**: Orange (#ea580c)

#### Typography Hierarchy
- **Dashboard Title**: 28px, Bold
- **Section Title**: 20px, Semi-bold  
- **Chart Title**: 16px, Semi-bold
- **Metric Value**: 24px, Bold, Monospace
- **Metric Change**: 14px, Medium

### Responsive Design Strategy

#### Breakpoint System
- **Desktop (>1200px)**: Full dashboard experience with sidebar
- **Tablet (768-1200px)**: Collapsible sidebar, single-column charts
- **Mobile (<768px)**: Card-based layout, simplified chart views

#### Mobile-Specific Components
- Swipeable KPI cards
- Tabbed chart sections  
- Simplified filter drawer
- Touch-optimized interactions

## Technical Visualization Architecture

### Chart Type Specifications

#### Risk & Credit Quality Dashboard

##### NPL Evolution Timeline
```javascript
{
  type: 'scatter',
  mode: 'lines+markers',
  x: quarterly_dates,
  y: npl_ratios,
  hovertemplate: '<b>%{fullData.name}</b><br>Period: %{x}<br>NPL Ratio: %{y:.2f}%<br>Portfolio: R$ %{customdata[0]:.1f}B<extra></extra>',
  line: { width: 3, color: riskColorScale },
  marker: { size: 8 }
}
```

##### Credit Concentration Heatmap
```javascript
{
  type: 'heatmap',
  x: credit_segments,
  y: institution_names,
  z: concentration_matrix,
  colorscale: 'RdYlBu_r',
  hoverongaps: false,
  hovertemplate: 'Institution: %{y}<br>Segment: %{x}<br>Concentration: %{z:.1f}%<extra></extra>'
}
```

#### Profitability & Efficiency Dashboard

##### ROE Decomposition Waterfall
```javascript
{
  type: 'waterfall',
  x: ['Asset Utilization', 'Profit Margin', 'Financial Leverage', 'Final ROE'],
  y: [asset_utilization, profit_margin, financial_leverage, final_roe],
  measure: ['relative', 'relative', 'relative', 'total'],
  hovertemplate: '%{x}<br>Contribution: %{y:.2f}pp<br>Cumulative: %{customdata:.2f}%<extra></extra>',
  connector: { line: { color: '#64748b', dash: 'dot' } }
}
```

##### Efficiency Frontier Scatter
```javascript
{
  type: 'scatter',
  x: cost_to_income_ratios,
  y: roe_values,
  mode: 'markers+text',
  text: institution_codes,
  textposition: 'top center',
  hovertemplate: '<b>%{text}</b><br>Cost/Income: %{x:.1f}%<br>ROE: %{y:.1f}%<br>Assets: R$ %{customdata[0]:.1f}B<extra></extra>',
  marker: {
    size: asset_sizes,
    sizemode: 'diameter',
    sizeref: 2,
    colorscale: 'Viridis'
  }
}
```

#### Capital & Regulatory Dashboard

##### Basel III Capital Ratios
```javascript
{
  type: 'bar',
  x: institution_names,
  y: [cet1_ratios, tier1_ratios, car_ratios],
  name: ['CET1', 'Tier 1', 'Total CAR'],
  hovertemplate: '<b>%{fullData.name}</b><br>Institution: %{x}<br>Ratio: %{y:.2f}%<br>Requirement: %{customdata[0]:.2f}%<extra></extra>',
  marker: { color: capitalColorPalette }
}
```

### Cross-Chart Interactivity

#### Dashboard State Management
```javascript
const dashboardState = {
  selectedInstitutions: ['BANCO_DO_BRASIL', 'ITAU_UNIBANCO'],
  timeRange: { start: '2022Q1', end: '2024Q3' },
  benchmarkType: 'peer_group',
  valueType: 'percentage',
  drillDownLevel: 1,
  activeFilters: { ... }
};

// Event handling for cross-chart updates
const handleChartSelection = (selectedData) => {
  updateDashboardState({
    selectedInstitutions: selectedData.points.map(p => p.customdata.institution_id),
    drillDownLevel: dashboardState.drillDownLevel + 1
  });
  
  // Update all charts in dashboard
  chartRefs.forEach(chart => chart.update(newData, newLayout));
};
```

### API Integration Patterns

#### RESTful Chart Data Endpoints
```python
# FastAPI backend endpoints
@app.get("/api/charts/npl-evolution")
async def get_npl_evolution(
    institutions: List[str] = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    benchmark_type: str = Query("peer")
) -> ChartDataResponse:
    """Return NPL evolution data formatted for Plotly"""
    
@app.get("/api/charts/roe-decomposition")
async def get_roe_decomposition(
    institutions: List[str] = Query(...),
    period: str = Query(...),
    comparison_type: str = Query("yoy")
) -> ChartDataResponse:
    """Return ROE decomposition waterfall data"""
```

#### React Integration Hooks
```javascript
// Custom hooks for chart data management
const useChartData = (chartType, filters) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchChartData(chartType, filters)
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [chartType, filters]);
  
  return { data, loading, error, refetch: () => fetchChartData(chartType, filters) };
};

// Dashboard component usage
const RiskDashboard = () => {
  const nplData = useChartData('npl-evolution', dashboardFilters);
  const concentrationData = useChartData('credit-concentration', dashboardFilters);
  
  return (
    <DashboardGrid>
      <PlotlyChart data={nplData.data} loading={nplData.loading} />
      <PlotlyChart data={concentrationData.data} loading={concentrationData.loading} />
    </DashboardGrid>
  );
};
```

### Performance Optimization

#### Data Management Strategies
- **Smart Sampling**: Reduce data points for large time series while preserving trends
- **Client Caching**: Cache chart data with TTL based on update frequency
- **Lazy Loading**: Load chart data only when dashboard sections are visible
- **Pagination**: Break large datasets into manageable chunks with navigation

#### Rendering Optimizations
- **WebGL Mode**: Enable for large datasets (>1000 points)
- **Partial Updates**: Update only changed data traces instead of full re-render
- **Debounced Interactions**: Prevent excessive API calls during filter changes
- **Virtual Scrolling**: For large institution lists and data tables

### Export Capabilities

#### Professional Chart Export
- **High-Quality PNG**: 300 DPI resolution for presentations
- **PDF Reports**: Multi-page reports with chart grids and metadata
- **Excel Integration**: Export underlying data with chart thumbnails
- **PowerPoint Ready**: Proper sizing and formatting for investment presentations

#### Data Export Options
- **CSV Format**: Raw data with headers and metadata
- **JSON Format**: Structured data for further analysis
- **API Access**: Direct data access for external tools
- **Scheduled Reports**: Automated report generation and distribution

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
**Deliverables**:
- Dashboard grid system and layout engine
- Advanced filter panel with state management
- Basic chart components with standard interactions
- API endpoint structure for chart data

**Key Components**:
- React dashboard framework
- Plotly.js integration layer
- Filter state management system
- Basic responsive design

### Phase 2: TIER 1 Dashboards (Weeks 5-12)

#### Weeks 5-6: Risk & Credit Quality Dashboard
- NPL evolution timeline with peer benchmarking
- Credit concentration heatmap with drill-down
- Provisioning analysis with coverage ratios
- Vintage cohort performance tracking

#### Weeks 7-8: Profitability & Efficiency Dashboard  
- ROE/ROA decomposition waterfall charts
- Efficiency frontier scatter plots with peer comparison
- NIM analysis with component breakdown
- Cost structure analysis with benchmarking

#### Weeks 9-10: Capital & Regulatory Dashboard
- Basel III capital ratios with regulatory thresholds
- Capital composition stacked charts
- Leverage ratio evolution with stress testing
- Risk-weighted asset analysis

#### Weeks 11-12: Integration & Testing
- Cross-dashboard navigation and state persistence
- Export functionality for all chart types
- Performance optimization and caching
- Comprehensive testing across browsers and devices

### Phase 3: Enhanced Features (Weeks 13-16)
**Deliverables**:
- Mobile responsiveness and touch optimization
- Advanced export capabilities (PDF reports, Excel)
- User preferences and dashboard customization
- Alert system for threshold monitoring

### Phase 4: Intelligence Layer (Weeks 17-20)
**Deliverables**:
- Smart suggestions based on user behavior
- Automated insights and anomaly detection
- Advanced benchmarking with peer group analysis
- Predictive indicators and trend extrapolation

## Success Metrics

### User Engagement KPIs
- **Dashboard Utilization**: % of users accessing each dashboard type monthly
- **Session Duration**: Average time spent in analysis workflows
- **Feature Adoption**: Usage rates for drill-down, filtering, and export features
- **User Retention**: Monthly/quarterly return rates for FSI professionals

### Business Impact Metrics
- **Decision Speed**: Reduction in time from data access to investment insight
- **Analysis Depth**: Number of drill-down interactions per session
- **Export Usage**: Frequency of chart/report exports for presentations
- **User Satisfaction**: Net Promoter Score from FSI professional feedback

### Technical Performance KPIs
- **Load Times**: <3 seconds for dashboard initial load, <1 second for chart updates
- **API Response**: <500ms for chart data endpoints
- **Error Rates**: <0.1% for chart rendering failures
- **Mobile Performance**: Lighthouse scores >90 for mobile usability

## Risk Mitigation

### Technical Risks
- **Performance with Large Datasets**: Implement progressive loading and data sampling
- **Cross-Browser Compatibility**: Comprehensive testing on major browsers/devices
- **API Reliability**: Implement retry logic and graceful degradation
- **Data Quality**: Validation and error handling for BACEN data inconsistencies

### User Experience Risks
- **Complexity Overwhelm**: Progressive disclosure and guided onboarding flows
- **Mobile Usability**: Simplified mobile interfaces with core functionality
- **Learning Curve**: Interactive tutorials and contextual help system
- **Performance Expectations**: Clear loading indicators and realistic performance targets

### Business Risks
- **Feature Scope Creep**: Strict adherence to TIER 1 priorities in initial release
- **User Adoption**: Early beta testing with target FSI professionals
- **Competitive Differentiation**: Focus on unique Brazilian banking insights
- **Regulatory Changes**: Flexible architecture to accommodate new BACEN requirements

## Next Steps

1. **Validate Plan**: Review with stakeholders and target users
2. **Technical Architecture**: Set up development environment and CI/CD
3. **Data Pipeline**: Prepare BACEN data processing for new chart requirements  
4. **Design System**: Create component library and design tokens
5. **Development Sprint Planning**: Break down phases into 2-week sprints
6. **Beta Testing Program**: Identify FSI professionals for early feedback
7. **Go-to-Market**: Plan launch strategy and user onboarding experience

---

*This plan positions Banco Insights 2.0 as the leading Brazilian banking intelligence platform for FSI professionals, combining comprehensive BACEN data coverage with professional-grade analytics and visualization capabilities.*