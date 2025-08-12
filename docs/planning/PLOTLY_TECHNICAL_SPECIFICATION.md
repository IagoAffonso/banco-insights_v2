# Plotly Technical Specification - Banco Insights 2.0
## Interactive Financial Visualizations for Brazilian Banking Intelligence

### Executive Summary

This document provides comprehensive technical specifications for Plotly-based interactive visualizations designed to support Banco Insights 2.0's three TIER 1 financial dashboards. The specification covers chart configurations, data structures, interactivity patterns, and integration approaches that work seamlessly across both current Streamlit (v1.0) and future React (v2.0) implementations.

---

## 1. Chart Type Specifications by Dashboard

### 1.1 Risk & Credit Quality Dashboard

#### 1.1.1 NPL Evolution Time Series
```javascript
// Plotly Configuration
{
  type: 'scatter',
  mode: 'lines+markers',
  data: [
    {
      x: ['2021Q1', '2021Q2', '2021Q3', '2021Q4', '2022Q1'],
      y: [2.1, 2.3, 2.8, 3.2, 2.9],
      name: 'Industry Average',
      line: { color: '#E74C3C', width: 3, dash: 'dash' },
      marker: { size: 8, color: '#E74C3C' }
    },
    {
      x: ['2021Q1', '2021Q2', '2021Q3', '2021Q4', '2022Q1'],
      y: [1.8, 1.9, 2.1, 2.4, 2.2],
      name: 'ITAU UNIBANCO',
      line: { color: '#3498DB', width: 2 },
      marker: { size: 6, color: '#3498DB' }
    }
  ],
  layout: {
    title: 'NPL Ratio Evolution (%)',
    xaxis: { title: 'Quarter', type: 'category' },
    yaxis: { title: 'NPL Ratio (%)', tickformat: '.1f' },
    hovermode: 'x unified',
    showlegend: true
  }
}
```

**Data Structure Required:**
```json
{
  "institution_name": "string",
  "quarter": "2024Q3",
  "npl_ratio": 2.3,
  "total_credit": 150000000000,
  "npl_amount": 3450000000,
  "benchmark_type": "industry|peer_group|top_tier"
}
```

#### 1.1.2 Credit Concentration Heatmap
```javascript
// Plotly Configuration
{
  type: 'heatmap',
  data: [{
    z: [[0.15, 0.23, 0.18], [0.12, 0.31, 0.22], [0.08, 0.19, 0.25]],
    x: ['Large Corporates', 'SME', 'Retail'],
    y: ['ITAU', 'BRADESCO', 'SANTANDER'],
    colorscale: [
      [0, '#2ECC71'], [0.5, '#F39C12'], [1, '#E74C3C']
    ],
    showscale: true,
    hoverongaps: false,
    hovertemplate: '%{y}<br>%{x}: %{z:.1%}<extra></extra>'
  }],
  layout: {
    title: 'Credit Portfolio Concentration by Segment',
    xaxis: { title: 'Credit Segments' },
    yaxis: { title: 'Financial Institutions' },
    height: 400
  }
}
```

#### 1.1.3 Provisioning Coverage Ratio
```javascript
// Plotly Configuration - Grouped Bar Chart
{
  data: [
    {
      x: ['ITAU', 'BRADESCO', 'SANTANDER', 'BANCO DO BRASIL'],
      y: [180, 165, 172, 155],
      name: 'Current Quarter',
      type: 'bar',
      marker: { color: '#3498DB' },
      hovertemplate: '%{x}<br>Coverage: %{y}%<extra></extra>'
    },
    {
      x: ['ITAU', 'BRADESCO', 'SANTANDER', 'BANCO DO BRASIL'],
      y: [175, 160, 168, 150],
      name: 'Previous Quarter',
      type: 'bar',
      marker: { color: '#95A5A6' },
      hovertemplate: '%{x}<br>Coverage: %{y}%<extra></extra>'
    }
  ],
  layout: {
    title: 'Provisioning Coverage Ratio Comparison (%)',
    barmode: 'group',
    xaxis: { title: 'Financial Institutions' },
    yaxis: { title: 'Coverage Ratio (%)' },
    showlegend: true
  }
}
```

### 1.2 Profitability & Efficiency Dashboard

#### 1.2.1 ROE Decomposition Waterfall
```javascript
// Plotly Configuration
{
  type: 'waterfall',
  data: [{
    name: 'ROE Decomposition',
    orientation: 'v',
    measure: ['relative', 'relative', 'relative', 'relative', 'total'],
    x: ['Net Margin', 'Asset Turnover', 'Equity Multiplier', 'Tax Effect', 'Total ROE'],
    textposition: 'outside',
    y: [2.1, 1.8, 3.2, -0.3, 6.8],
    connector: { line: { color: 'rgb(63, 63, 63)' } },
    decreasing: { marker: { color: '#E74C3C' } },
    increasing: { marker: { color: '#2ECC71' } },
    totals: { marker: { color: '#3498DB' } }
  }],
  layout: {
    title: 'ROE Decomposition Analysis (%)',
    showlegend: false,
    xaxis: { type: 'category' },
    yaxis: { title: 'ROE Components (%)' }
  }
}
```

#### 1.2.2 NIM Trend Analysis
```javascript
// Plotly Configuration - Multi-line with Fill
{
  data: [
    {
      x: ['2022Q1', '2022Q2', '2022Q3', '2022Q4', '2023Q1'],
      y: [4.2, 4.5, 4.8, 5.1, 4.9],
      fill: 'tonexty',
      type: 'scatter',
      mode: 'lines',
      name: 'Top Quartile',
      line: { color: '#2ECC71' }
    },
    {
      x: ['2022Q1', '2022Q2', '2022Q3', '2022Q4', '2023Q1'],
      y: [3.1, 3.3, 3.6, 3.8, 3.7],
      fill: 'tozeroy',
      type: 'scatter',
      mode: 'lines',
      name: 'Bottom Quartile',
      line: { color: '#E74C3C' }
    }
  ],
  layout: {
    title: 'Net Interest Margin Distribution (%)',
    xaxis: { title: 'Quarter' },
    yaxis: { title: 'NIM (%)' },
    hovermode: 'x unified'
  }
}
```

#### 1.2.3 Cost-to-Income Efficiency Scatter
```javascript
// Plotly Configuration
{
  data: [{
    x: [45, 52, 38, 62, 48, 55],
    y: [12.5, 8.3, 15.2, 6.1, 11.8, 9.4],
    mode: 'markers+text',
    type: 'scatter',
    text: ['ITAU', 'BRADESCO', 'NUBANK', 'BANCO DO BRASIL', 'SANTANDER', 'BTG'],
    textposition: 'top center',
    marker: {
      size: 15,
      color: [45, 52, 38, 62, 48, 55],
      colorscale: 'RdYlGn',
      reversescale: true,
      showscale: true,
      colorbar: { title: 'Efficiency Ratio (%)' }
    },
    hovertemplate: '%{text}<br>Efficiency: %{x}%<br>ROE: %{y}%<extra></extra>'
  }],
  layout: {
    title: 'Efficiency vs Profitability Analysis',
    xaxis: { title: 'Cost-to-Income Ratio (%)' },
    yaxis: { title: 'ROE (%)' },
    showlegend: false
  }
}
```

### 1.3 Capital & Regulatory Dashboard

#### 1.3.1 Basel III Capital Stacked Bar
```javascript
// Plotly Configuration
{
  data: [
    {
      x: ['ITAU', 'BRADESCO', 'SANTANDER', 'BANCO DO BRASIL'],
      y: [8.5, 8.2, 8.8, 8.0],
      name: 'CET1',
      type: 'bar',
      marker: { color: '#2ECC71' }
    },
    {
      x: ['ITAU', 'BRADESCO', 'SANTANDER', 'BANCO DO BRASIL'],
      y: [1.5, 1.8, 1.2, 2.0],
      name: 'Additional Tier 1',
      type: 'bar',
      marker: { color: '#F39C12' }
    },
    {
      x: ['ITAU', 'BRADESCO', 'SANTANDER', 'BANCO DO BRASIL'],
      y: [2.0, 2.2, 1.8, 2.5],
      name: 'Tier 2',
      type: 'bar',
      marker: { color: '#3498DB' }
    }
  ],
  layout: {
    title: 'Basel III Capital Composition (%)',
    barmode: 'stack',
    xaxis: { title: 'Financial Institutions' },
    yaxis: { title: 'Capital Ratio (%)' },
    showlegend: true
  }
}
```

#### 1.3.2 Leverage Ratio Evolution
```javascript
// Plotly Configuration - Area Chart
{
  data: [
    {
      x: ['2022Q1', '2022Q2', '2022Q3', '2022Q4', '2023Q1'],
      y: [6.2, 6.5, 6.8, 7.1, 6.9],
      fill: 'tonexty',
      type: 'scatter',
      mode: 'lines',
      name: 'ITAU',
      line: { color: '#3498DB' }
    },
    {
      x: ['2022Q1', '2022Q2', '2022Q3', '2022Q4', '2023Q1'],
      y: [5.8, 6.0, 6.3, 6.6, 6.4],
      fill: 'tozeroy',
      type: 'scatter',
      mode: 'lines',
      name: 'Industry Average',
      line: { color: '#95A5A6', dash: 'dash' }
    }
  ],
  layout: {
    title: 'Leverage Ratio Evolution (%)',
    xaxis: { title: 'Quarter' },
    yaxis: { title: 'Leverage Ratio (%)' },
    hovermode: 'x unified'
  }
}
```

---

## 2. Interactive Features & Behaviors

### 2.1 Hover Interactions
```javascript
// Standard hover template for financial metrics
const hoverTemplate = {
  basic: '%{x}<br>%{fullData.name}: %{y}<extra></extra>',
  financial: '%{x}<br>%{fullData.name}: %{y:.2f}%<br>Amount: R$ %{customdata:.0s}<extra></extra>',
  comparison: '%{x}<br>Institution: %{fullData.name}<br>Value: %{y:.2f}<br>Benchmark: %{customdata:.2f}<extra></extra>'
};

// Enhanced hover with additional context
const enhancedHover = {
  hovermode: 'x unified',
  hoverdistance: 100,
  spikedistance: 1000,
  xaxis: {
    showspikes: true,
    spikemode: 'across',
    spikesnap: 'cursor'
  },
  yaxis: {
    showspikes: true,
    spikemode: 'across'
  }
};
```

### 2.2 Click Behaviors
```javascript
// Drill-down functionality
const clickHandlers = {
  // Time series drill-down
  timeSeriesClick: function(data) {
    const clickedQuarter = data.points[0].x;
    const institution = data.points[0].data.name;
    
    // Trigger detailed breakdown for that quarter
    loadDetailedBreakdown(institution, clickedQuarter);
  },
  
  // Institution comparison
  institutionClick: function(data) {
    const institution = data.points[0].x;
    
    // Add/remove from comparison set
    toggleInstitutionComparison(institution);
  },
  
  // Segment drill-down
  segmentClick: function(data) {
    const segment = data.points[0].data.name;
    
    // Load segment-specific analysis
    loadSegmentAnalysis(segment);
  }
};
```

### 2.3 Selection Tools
```javascript
// Range selection for time series
const selectionConfig = {
  rangeslider: {
    visible: true,
    range: ['2020-01-01', '2024-12-31']
  },
  rangeselector: {
    buttons: [
      { count: 4, label: '1Y', step: 'quarter', stepmode: 'backward' },
      { count: 8, label: '2Y', step: 'quarter', stepmode: 'backward' },
      { count: 12, label: '3Y', step: 'quarter', stepmode: 'backward' },
      { step: 'all' }
    ]
  }
};

// Brush selection for scatter plots
const brushSelection = {
  dragmode: 'select',
  showTips: false,
  newshape: {
    drawdirection: 'diagonal',
    fillcolor: 'rgba(0,100,80,0.2)',
    fillrule: 'evenodd',
    line: { color: 'rgba(0,100,80,1)', width: 2 },
    opacity: 0.8
  }
};
```

### 2.4 Zoom & Pan Configuration
```javascript
const zoomPanConfig = {
  // Enable zoom and pan
  scrollZoom: true,
  doubleClick: 'reset+autosize',
  showTips: false,
  
  // Constrain interactions
  xaxis: {
    fixedrange: false,
    rangeslider: { visible: false } // Hide for dashboard views
  },
  yaxis: {
    fixedrange: false
  },
  
  // Responsive sizing
  autosize: true,
  responsive: true
};
```

---

## 3. Cross-Chart Interactivity Patterns

### 3.1 Dashboard State Management
```javascript
// Global dashboard state
class DashboardState {
  constructor() {
    this.selectedInstitutions = [];
    this.selectedPeriod = '2024Q3';
    this.comparisonMode = 'peer_group';
    this.filters = {
      institution_type: 'all',
      asset_size: 'all',
      geography: 'all'
    };
  }

  // Update all charts when state changes
  updateAllCharts() {
    const charts = document.querySelectorAll('[data-chart-id]');
    charts.forEach(chart => {
      this.updateChart(chart.dataset.chartId);
    });
  }

  // Individual chart update
  updateChart(chartId) {
    const chartConfig = this.getChartConfig(chartId);
    Plotly.react(chartId, chartConfig.data, chartConfig.layout);
  }
}
```

### 3.2 Filter Synchronization
```javascript
// Synchronized filtering across charts
const filterSync = {
  // Institution filter
  onInstitutionFilter: function(selectedInstitutions) {
    dashboardState.selectedInstitutions = selectedInstitutions;
    
    // Update all charts with new institution filter
    Promise.all([
      updateRiskCharts(selectedInstitutions),
      updateProfitabilityCharts(selectedInstitutions),
      updateCapitalCharts(selectedInstitutions)
    ]);
  },
  
  // Time period filter
  onPeriodFilter: function(startPeriod, endPeriod) {
    dashboardState.timePeriod = { start: startPeriod, end: endPeriod };
    
    // Update time-series charts
    updateTimeSeriesCharts(startPeriod, endPeriod);
  },
  
  // Benchmark filter
  onBenchmarkFilter: function(benchmarkType) {
    dashboardState.comparisonMode = benchmarkType;
    
    // Reload benchmark data for all charts
    reloadBenchmarkData(benchmarkType);
  }
};
```

### 3.3 Linked Selections
```javascript
// Cross-chart selections
const linkedSelections = {
  // Select institution in one chart, highlight in all others
  linkInstitutionSelection: function(institution) {
    const allCharts = document.querySelectorAll('[data-chart-type]');
    
    allCharts.forEach(chart => {
      const chartDiv = document.getElementById(chart.id);
      const data = chartDiv.data;
      
      // Update opacity for non-selected institutions
      data.forEach((trace, index) => {
        if (trace.name === institution) {
          trace.opacity = 1.0;
          trace.line.width = 4;
        } else {
          trace.opacity = 0.3;
          trace.line.width = 2;
        }
      });
      
      Plotly.redraw(chart.id);
    });
  },
  
  // Brush selection synchronization
  linkBrushSelection: function(selectedPoints, sourceChart) {
    const institutions = selectedPoints.map(p => p.data.name);
    
    // Update other charts to highlight selected institutions
    this.linkInstitutionSelection(institutions);
  }
};
```

---

## 4. Data Structure Requirements

### 4.1 Time Series Data Format
```json
{
  "time_series_data": {
    "metadata": {
      "metric_name": "NPL_Ratio",
      "unit": "percentage",
      "frequency": "quarterly",
      "last_updated": "2024-08-10T10:00:00Z"
    },
    "series": [
      {
        "institution_id": "ITAU_001",
        "institution_name": "ITAU UNIBANCO S.A.",
        "data_points": [
          {
            "period": "2024Q1",
            "value": 2.3,
            "benchmark_value": 2.8,
            "percentile": 25,
            "raw_amount": 15000000000
          }
        ]
      }
    ]
  }
}
```

### 4.2 Cross-Sectional Data Format
```json
{
  "cross_sectional_data": {
    "metadata": {
      "period": "2024Q3",
      "metric_categories": ["efficiency", "profitability", "risk"],
      "total_institutions": 150
    },
    "institutions": [
      {
        "institution_id": "ITAU_001",
        "institution_name": "ITAU UNIBANCO S.A.",
        "institution_type": "Commercial Bank",
        "asset_size_tier": "Large",
        "metrics": {
          "cost_income_ratio": 45.2,
          "roe": 12.5,
          "npl_ratio": 2.1,
          "tier1_capital": 13.8
        },
        "benchmarks": {
          "peer_group": {
            "cost_income_ratio": 48.1,
            "roe": 11.2,
            "npl_ratio": 2.4
          },
          "industry": {
            "cost_income_ratio": 52.3,
            "roe": 9.8,
            "npl_ratio": 2.9
          }
        }
      }
    ]
  }
}
```

### 4.3 Hierarchical Data Format (for drill-downs)
```json
{
  "hierarchical_data": {
    "institution_id": "ITAU_001",
    "period": "2024Q3",
    "credit_portfolio": {
      "total": 850000000000,
      "segments": {
        "retail": {
          "total": 450000000000,
          "subsegments": {
            "mortgage": 180000000000,
            "personal_loans": 120000000000,
            "credit_cards": 100000000000,
            "vehicle_finance": 50000000000
          }
        },
        "corporate": {
          "total": 400000000000,
          "subsegments": {
            "large_corporate": 250000000000,
            "sme": 100000000000,
            "commercial_real_estate": 50000000000
          }
        }
      }
    }
  }
}
```

---

## 5. API Integration Patterns

### 5.1 RESTful Endpoint Structure
```python
# FastAPI Endpoint Pattern
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import plotly.graph_objects as go

@app.get("/api/v2/charts/{dashboard_type}/{chart_type}")
async def get_chart_data(
    dashboard_type: str,  # risk, profitability, capital
    chart_type: str,      # npl_evolution, roe_decomposition, etc.
    institutions: List[str] = Query(...),
    start_period: str = Query("2020Q1"),
    end_period: str = Query("2024Q3"),
    benchmark_type: str = Query("peer_group"),
    format_type: str = Query("plotly_json")  # plotly_json, raw_data, csv
):
    try:
        # Get data from database
        data = await get_chart_data_from_db(
            dashboard_type, chart_type, institutions,
            start_period, end_period, benchmark_type
        )
        
        # Generate Plotly figure
        fig = create_chart(chart_type, data)
        
        if format_type == "plotly_json":
            return {"figure_json": fig.to_json()}
        elif format_type == "raw_data":
            return {"data": data}
        else:
            raise HTTPException(status_code=400, detail="Invalid format_type")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 5.2 WebSocket Pattern for Real-time Updates
```python
# WebSocket for dashboard updates
from fastapi import WebSocket
import asyncio
import json

@app.websocket("/ws/dashboard/{dashboard_id}")
async def dashboard_websocket(websocket: WebSocket, dashboard_id: str):
    await websocket.accept()
    
    try:
        while True:
            # Listen for client requests
            request = await websocket.receive_text()
            request_data = json.loads(request)
            
            # Process request and get updated data
            if request_data["type"] == "filter_update":
                updated_data = await process_filter_update(
                    dashboard_id, request_data["filters"]
                )
                
                # Send updated chart data
                await websocket.send_text(json.dumps({
                    "type": "chart_update",
                    "charts": updated_data
                }))
                
    except Exception as e:
        await websocket.close()
```

### 5.3 React Integration Pattern
```jsx
// React Hook for Plotly Integration
import { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js-dist';

export const useplotlyChart = (chartConfig, dependencies = []) => {
  const plotRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!plotRef.current || !chartConfig) return;

    setIsLoading(true);
    
    // Create or update the plot
    Plotly.react(
      plotRef.current,
      chartConfig.data,
      chartConfig.layout,
      chartConfig.config || {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
        toImageButtonOptions: {
          format: 'png',
          filename: 'banco_insights_chart',
          height: 600,
          width: 1200,
          scale: 2
        }
      }
    ).then(() => {
      setIsLoading(false);
    });

    // Add event listeners
    plotRef.current.on('plotly_click', (data) => {
      if (chartConfig.onClick) {
        chartConfig.onClick(data);
      }
    });

    plotRef.current.on('plotly_hover', (data) => {
      if (chartConfig.onHover) {
        chartConfig.onHover(data);
      }
    });

  }, [chartConfig, ...dependencies]);

  return { plotRef, isLoading };
};

// Dashboard Component
export const RiskDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [filters, setFilters] = useState({
    institutions: ['ITAU', 'BRADESCO'],
    period: '2024Q3',
    benchmarkType: 'peer_group'
  });

  // Fetch chart configurations
  const { data: nplChart } = useFetch(`/api/v2/charts/risk/npl_evolution?${queryString}`);
  const { data: provisioningChart } = useFetch(`/api/v2/charts/risk/provisioning_coverage?${queryString}`);

  const nplChartRef = useplotlyChart(nplChart, [filters]);
  const provisioningChartRef = useplotlyChart(provisioningChart, [filters]);

  return (
    <div className="dashboard-grid">
      <div className="chart-container">
        <h3>NPL Evolution</h3>
        <div ref={nplChartRef.plotRef} />
        {nplChartRef.isLoading && <div className="loading-spinner" />}
      </div>
      
      <div className="chart-container">
        <h3>Provisioning Coverage</h3>
        <div ref={provisioningChartRef.plotRef} />
        {provisioningChartRef.isLoading && <div className="loading-spinner" />}
      </div>
    </div>
  );
};
```

---

## 6. Performance Optimization Strategies

### 6.1 Data Sampling and Aggregation
```python
# Smart data sampling for large datasets
def optimize_data_for_visualization(df, chart_type, max_points=1000):
    """
    Optimize data for visualization based on chart type and data size
    """
    if len(df) <= max_points:
        return df
    
    if chart_type == "time_series":
        # For time series, use time-based sampling
        return sample_time_series(df, max_points)
    
    elif chart_type == "scatter":
        # For scatter plots, use density-based sampling
        return sample_scatter_density(df, max_points)
    
    elif chart_type == "heatmap":
        # For heatmaps, use aggregation
        return aggregate_heatmap_data(df, max_points)
    
    return df.sample(n=max_points)

def sample_time_series(df, max_points):
    """Sample time series data intelligently"""
    if len(df) <= max_points:
        return df
    
    # Keep all recent data, sample older data
    recent_cutoff = df['period'].max() - pd.DateOffset(years=1)
    recent_data = df[df['period'] >= recent_cutoff]
    older_data = df[df['period'] < recent_cutoff]
    
    # Sample older data
    sample_size = max_points - len(recent_data)
    if sample_size > 0:
        sampled_older = older_data.sample(n=min(sample_size, len(older_data)))
        return pd.concat([sampled_older, recent_data]).sort_values('period')
    
    return recent_data.tail(max_points)
```

### 6.2 Client-Side Caching
```javascript
// Chart data caching with TTL
class ChartDataCache {
  constructor() {
    this.cache = new Map();
    this.ttl = 5 * 60 * 1000; // 5 minutes TTL
  }

  getCacheKey(chartType, filters) {
    return `${chartType}_${JSON.stringify(filters)}`;
  }

  get(chartType, filters) {
    const key = this.getCacheKey(chartType, filters);
    const cached = this.cache.get(key);
    
    if (cached && Date.now() - cached.timestamp < this.ttl) {
      return cached.data;
    }
    
    return null;
  }

  set(chartType, filters, data) {
    const key = this.getCacheKey(chartType, filters);
    this.cache.set(key, {
      data: data,
      timestamp: Date.now()
    });
  }

  clear() {
    this.cache.clear();
  }
}

const chartCache = new ChartDataCache();
```

### 6.3 Lazy Loading and Virtualization
```jsx
// Lazy loading for dashboard sections
import { lazy, Suspense } from 'react';
import { useInView } from 'react-intersection-observer';

const RiskCharts = lazy(() => import('./RiskCharts'));
const ProfitabilityCharts = lazy(() => import('./ProfitabilityCharts'));
const CapitalCharts = lazy(() => import('./CapitalCharts'));

export const Dashboard = () => {
  const [riskRef, riskInView] = useInView({ triggerOnce: true, threshold: 0.1 });
  const [profitRef, profitInView] = useInView({ triggerOnce: true, threshold: 0.1 });
  const [capitalRef, capitalInView] = useInView({ triggerOnce: true, threshold: 0.1 });

  return (
    <div className="dashboard">
      <div ref={riskRef}>
        <Suspense fallback={<div>Loading Risk Charts...</div>}>
          {riskInView && <RiskCharts />}
        </Suspense>
      </div>
      
      <div ref={profitRef}>
        <Suspense fallback={<div>Loading Profitability Charts...</div>}>
          {profitInView && <ProfitabilityCharts />}
        </Suspense>
      </div>
      
      <div ref={capitalRef}>
        <Suspense fallback={<div>Loading Capital Charts...</div>}>
          {capitalInView && <CapitalCharts />}
        </Suspense>
      </div>
    </div>
  );
};
```

### 6.4 Server-Side Rendering Optimization
```python
# Pre-compute chart configurations
import asyncio
from functools import lru_cache

@lru_cache(maxsize=128)
def get_static_chart_layout(chart_type):
    """Cache static chart layouts"""
    layouts = {
        'npl_evolution': {
            'title': 'NPL Ratio Evolution (%)',
            'xaxis': {'title': 'Quarter', 'type': 'category'},
            'yaxis': {'title': 'NPL Ratio (%)', 'tickformat': '.1f'},
            'hovermode': 'x unified'
        }
        # ... other layouts
    }
    return layouts.get(chart_type, {})

async def pre_compute_chart_data():
    """Pre-compute frequently accessed chart data"""
    common_combinations = [
        {'institutions': ['ITAU', 'BRADESCO', 'SANTANDER'], 'chart_type': 'npl_evolution'},
        {'institutions': ['BANCO DO BRASIL', 'CAIXA'], 'chart_type': 'roe_decomposition'}
    ]
    
    tasks = []
    for combo in common_combinations:
        task = compute_and_cache_chart(combo)
        tasks.append(task)
    
    await asyncio.gather(*tasks)
```

---

## 7. Export Capabilities

### 7.1 Professional Chart Export
```javascript
// High-quality export configuration
const exportConfig = {
  // PNG Export with high DPI
  toPNG: {
    format: 'png',
    width: 1200,
    height: 800,
    scale: 2, // High DPI for print quality
    engine: 'kaleido'
  },
  
  // PDF Export with vector graphics
  toPDF: {
    format: 'pdf',
    width: 11.7, // A4 width in inches
    height: 8.3,  // A4 height in inches
    engine: 'kaleido'
  },
  
  // SVG for scalable graphics
  toSVG: {
    format: 'svg',
    width: 1200,
    height: 800,
    engine: 'kaleido'
  }
};

// Export function with branding
function exportChartWithBranding(plotDiv, format = 'png', options = {}) {
  const config = {
    ...exportConfig[format === 'png' ? 'toPNG' : format === 'pdf' ? 'toPDF' : 'toSVG'],
    ...options
  };
  
  // Add watermark/branding
  const layout = plotDiv.layout;
  layout.annotations = layout.annotations || [];
  layout.annotations.push({
    text: 'Banco Insights 2.0 - Brazilian Banking Intelligence',
    x: 1,
    y: 0,
    xref: 'paper',
    yref: 'paper',
    xanchor: 'right',
    yanchor: 'bottom',
    showarrow: false,
    font: { size: 10, color: '#666' }
  });
  
  return Plotly.toImage(plotDiv, config);
}
```

### 7.2 Data Export with Metadata
```python
# Comprehensive data export
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Font, Alignment

def export_dashboard_data(dashboard_type, filters, format='excel'):
    """
    Export dashboard data with charts and metadata
    """
    if format == 'excel':
        return export_to_excel(dashboard_type, filters)
    elif format == 'csv':
        return export_to_csv(dashboard_type, filters)
    elif format == 'json':
        return export_to_json(dashboard_type, filters)

def export_to_excel(dashboard_type, filters):
    """Export to Excel with multiple sheets and embedded charts"""
    wb = Workbook()
    
    # Remove default sheet
    wb.remove(wb.active)
    
    # Get data for all charts in dashboard
    chart_data = get_dashboard_data(dashboard_type, filters)
    
    # Create sheets for each chart
    for chart_name, data in chart_data.items():
        ws = wb.create_sheet(title=chart_name[:31])  # Excel sheet name limit
        
        # Write data
        df = pd.DataFrame(data['data'])
        for r_idx, row in enumerate(df.values, 2):
            for c_idx, value in enumerate(row, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)
        
        # Write headers
        for c_idx, header in enumerate(df.columns, 1):
            cell = ws.cell(row=1, column=c_idx, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # Add metadata sheet
        metadata_ws = wb.create_sheet(title='Metadata')
        metadata = [
            ['Dashboard Type', dashboard_type],
            ['Export Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Institutions', ', '.join(filters.get('institutions', []))],
            ['Period Range', f"{filters.get('start_period')} - {filters.get('end_period')}"],
            ['Data Source', 'BACEN IF.data'],
            ['Generated by', 'Banco Insights 2.0']
        ]
        
        for r_idx, (key, value) in enumerate(metadata, 1):
            metadata_ws.cell(row=r_idx, column=1, value=key).font = Font(bold=True)
            metadata_ws.cell(row=r_idx, column=2, value=value)
    
    # Save to BytesIO
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return excel_file

# API endpoint for exports
@app.get("/api/v2/export/{dashboard_type}")
async def export_dashboard(
    dashboard_type: str,
    format: str = Query("excel", enum=["excel", "csv", "json", "pdf"]),
    institutions: List[str] = Query(...),
    start_period: str = Query("2020Q1"),
    end_period: str = Query("2024Q3")
):
    try:
        filters = {
            'institutions': institutions,
            'start_period': start_period,
            'end_period': end_period
        }
        
        export_data = export_dashboard_data(dashboard_type, filters, format)
        
        headers = {
            'Content-Disposition': f'attachment; filename="banco_insights_{dashboard_type}_{datetime.now().strftime("%Y%m%d")}.{format}"'
        }
        
        if format == 'excel':
            return Response(export_data.getvalue(), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)
        elif format == 'csv':
            return Response(export_data, media_type='text/csv', headers=headers)
        elif format == 'json':
            return Response(json.dumps(export_data), media_type='application/json', headers=headers)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 8. Responsive Design Patterns

### 8.1 Breakpoint-Aware Chart Sizing
```javascript
// Responsive chart configuration
const responsiveConfig = {
  // Mobile breakpoint adjustments
  mobile: {
    layout: {
      height: 300,
      margin: { l: 40, r: 20, t: 40, b: 40 },
      legend: {
        orientation: 'h',
        x: 0,
        y: -0.2
      },
      font: { size: 10 }
    },
    config: {
      displayModeBar: false
    }
  },
  
  // Tablet breakpoint adjustments  
  tablet: {
    layout: {
      height: 400,
      margin: { l: 50, r: 30, t: 50, b: 50 },
      font: { size: 12 }
    },
    config: {
      displayModeBar: true,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'autoScale2d']
    }
  },
  
  // Desktop configuration
  desktop: {
    layout: {
      height: 500,
      margin: { l: 60, r: 40, t: 60, b: 60 },
      font: { size: 14 }
    },
    config: {
      displayModeBar: true
    }
  }
};

// Apply responsive configuration based on screen size
function getResponsiveConfig() {
  const width = window.innerWidth;
  
  if (width < 768) {
    return responsiveConfig.mobile;
  } else if (width < 1024) {
    return responsiveConfig.tablet;
  } else {
    return responsiveConfig.desktop;
  }
}

// Update charts on window resize
window.addEventListener('resize', debounce(() => {
  const charts = document.querySelectorAll('[data-chart-id]');
  charts.forEach(chart => {
    const config = getResponsiveConfig();
    Plotly.relayout(chart, config.layout);
  });
}, 250));
```

### 8.2 Touch-Friendly Interactions
```javascript
// Mobile-optimized interaction configuration
const mobileInteractionConfig = {
  // Larger touch targets
  hoverdistance: 50,
  spikedistance: -1,
  
  // Touch-friendly drag modes
  dragmode: 'pan',
  
  // Simplified hover
  hovermode: 'x',
  
  // Touch gestures
  scrollZoom: true,
  doubleClick: 'reset',
  
  // Simplified toolbar
  displayModeBar: 'hover',
  modeBarButtonsToRemove: [
    'select2d',
    'lasso2d', 
    'autoScale2d',
    'hoverClosestCartesian',
    'hoverCompareCartesian',
    'toggleSpikelines'
  ]
};
```

---

## 9. Color Schemes and Theming

### 9.1 Professional Financial Color Palette
```javascript
const colorSchemes = {
  // Primary brand colors
  primary: {
    blue: '#2C5AA0',      // Trust, stability
    green: '#27AE60',     // Growth, positive performance  
    red: '#E74C3C',       // Risk, negative performance
    orange: '#F39C12',    // Warning, attention
    gray: '#7F8C8D'       // Neutral, benchmarks
  },
  
  // Institution-specific colors (top 10 banks)
  institutions: {
    'ITAU UNIBANCO': '#EC7000',
    'BANCO DO BRASIL': '#FFD700', 
    'BRADESCO': '#CC092F',
    'SANTANDER': '#EA2128',
    'CAIXA ECONOMICA FEDERAL': '#0066CC',
    'BTG PACTUAL': '#000000',
    'NUBANK': '#8A05BE',
    'XP INVESTIMENTOS': '#F78C40',
    'INTER': '#FF7A00',
    'C6 BANK': '#FFD700'
  },
  
  // Risk-based color gradients
  risk: {
    low: '#27AE60',
    medium_low: '#F39C12', 
    medium: '#E67E22',
    medium_high: '#E74C3C',
    high: '#C0392B'
  },
  
  // Performance gradients
  performance: [
    '#C0392B', // Bottom quartile
    '#E74C3C', // Below average
    '#F39C12', // Average
    '#27AE60', // Above average  
    '#1E8449'  // Top quartile
  ],
  
  // Accessible color palette (colorblind-friendly)
  accessible: [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf'
  ]
};

// Dark theme for professional presentations
const darkTheme = {
  paper_bgcolor: '#1e1e1e',
  plot_bgcolor: '#2d2d2d', 
  font: { color: '#ffffff' },
  gridcolor: '#444444',
  zerolinecolor: '#666666'
};

// Light theme for reports and documents
const lightTheme = {
  paper_bgcolor: '#ffffff',
  plot_bgcolor: '#fafafa',
  font: { color: '#2c3e50' },
  gridcolor: '#e0e0e0', 
  zerolinecolor: '#bdbdbd'
};
```

---

## 10. Implementation Guidelines

### 10.1 Migration from Streamlit to React
```python
# Shared utility functions for both platforms
class PlotlyConfigGenerator:
    """Generate Plotly configurations that work in both Streamlit and React"""
    
    def __init__(self, theme='light'):
        self.theme = theme
        self.base_config = {
            'responsive': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape']
        }
    
    def generate_time_series_config(self, data, chart_type='line'):
        """Generate time series chart configuration"""
        config = {
            'data': self._format_time_series_data(data, chart_type),
            'layout': self._get_time_series_layout(),
            'config': self.base_config
        }
        return config
    
    def generate_comparison_config(self, data, comparison_type='bar'):
        """Generate comparison chart configuration"""
        config = {
            'data': self._format_comparison_data(data, comparison_type),
            'layout': self._get_comparison_layout(),
            'config': self.base_config
        }
        return config
    
    def _format_time_series_data(self, data, chart_type):
        """Format data for time series charts"""
        traces = []
        for institution in data['institutions']:
            trace = {
                'x': data['periods'],
                'y': institution['values'],
                'name': institution['name'],
                'type': 'scatter',
                'mode': 'lines+markers' if chart_type == 'line' else 'markers',
                'line': {'width': 2},
                'marker': {'size': 6}
            }
            traces.append(trace)
        return traces

# Usage in both Streamlit and React
def create_npl_chart(data):
    generator = PlotlyConfigGenerator()
    return generator.generate_time_series_config(data, 'line')

# Streamlit implementation
import streamlit as st
import plotly.graph_objects as go

def streamlit_chart(chart_config):
    fig = go.Figure(
        data=chart_config['data'],
        layout=chart_config['layout']
    )
    st.plotly_chart(fig, use_container_width=True, config=chart_config['config'])

# React implementation would use the same chart_config
# const ReactChart = ({ chartConfig }) => {
#   const { plotRef } = useplotlyChart(chartConfig);
#   return <div ref={plotRef} />;
# };
```

### 10.2 Testing Strategy
```python
# Automated chart testing
import pytest
from plotly.graph_objects import Figure

class TestChartGeneration:
    """Test chart generation functions"""
    
    @pytest.fixture
    def sample_data(self):
        return {
            'institutions': [
                {'name': 'ITAU', 'values': [2.1, 2.3, 2.0, 1.9]},
                {'name': 'BRADESCO', 'values': [2.5, 2.7, 2.4, 2.2]}
            ],
            'periods': ['2024Q1', '2024Q2', '2024Q3', '2024Q4']
        }
    
    def test_npl_chart_generation(self, sample_data):
        """Test NPL chart generation"""
        config = create_npl_chart(sample_data)
        
        # Validate configuration structure
        assert 'data' in config
        assert 'layout' in config
        assert 'config' in config
        
        # Validate data format
        assert len(config['data']) == 2
        assert all('x' in trace and 'y' in trace for trace in config['data'])
        
        # Create figure and validate
        fig = Figure(data=config['data'], layout=config['layout'])
        assert isinstance(fig, Figure)
        
        # Test that figure can be serialized to JSON
        json_str = fig.to_json()
        assert json_str is not None
    
    def test_chart_responsiveness(self, sample_data):
        """Test responsive chart configuration"""
        mobile_config = get_responsive_config('mobile')
        desktop_config = get_responsive_config('desktop')
        
        assert mobile_config['layout']['height'] < desktop_config['layout']['height']
        assert mobile_config['layout']['font']['size'] < desktop_config['layout']['font']['size']
    
    @pytest.mark.parametrize("chart_type", ['npl_evolution', 'roe_decomposition', 'capital_ratios'])
    def test_all_chart_types(self, chart_type, sample_data):
        """Test all chart types generate valid configurations"""
        config = generate_chart_config(chart_type, sample_data)
        
        # Validate all charts have required structure
        assert isinstance(config, dict)
        assert 'data' in config
        assert 'layout' in config
        
        # Validate JSON serialization
        fig = Figure(data=config['data'], layout=config['layout'])
        json_str = fig.to_json()
        assert len(json_str) > 0
```

---

## 11. Security and Compliance Considerations

### 11.1 Data Privacy and Access Control
```python
# Role-based chart access
from enum import Enum

class AccessLevel(Enum):
    PUBLIC = "public"          # Public market data
    INTERNAL = "internal"      # Internal analysis
    CONFIDENTIAL = "confidential"  # Sensitive metrics

class ChartAccessControl:
    """Control access to different chart types based on user permissions"""
    
    def __init__(self):
        self.chart_permissions = {
            'market_share': AccessLevel.PUBLIC,
            'npl_evolution': AccessLevel.INTERNAL,
            'profitability_analysis': AccessLevel.CONFIDENTIAL,
            'regulatory_capital': AccessLevel.INTERNAL
        }
    
    def can_access_chart(self, user_role: str, chart_type: str) -> bool:
        """Check if user can access specific chart type"""
        required_level = self.chart_permissions.get(chart_type, AccessLevel.CONFIDENTIAL)
        
        role_permissions = {
            'viewer': [AccessLevel.PUBLIC],
            'analyst': [AccessLevel.PUBLIC, AccessLevel.INTERNAL],
            'senior_analyst': [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL]
        }
        
        user_permissions = role_permissions.get(user_role, [])
        return required_level in user_permissions
    
    def filter_chart_data(self, chart_data: dict, user_role: str) -> dict:
        """Filter sensitive data based on user role"""
        if user_role == 'viewer':
            # Remove detailed breakdowns for public users
            chart_data = self._anonymize_institution_names(chart_data)
        
        return chart_data

# API endpoint with access control
@app.get("/api/v2/charts/{chart_type}")
async def get_secure_chart(
    chart_type: str,
    current_user: User = Depends(get_current_user)
):
    access_control = ChartAccessControl()
    
    if not access_control.can_access_chart(current_user.role, chart_type):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Get and filter data based on user role
    raw_data = await get_chart_data(chart_type)
    filtered_data = access_control.filter_chart_data(raw_data, current_user.role)
    
    return {"figure_json": generate_chart(chart_type, filtered_data)}
```

### 11.2 Data Validation and Sanitization
```python
# Input validation for chart parameters
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class ChartRequest(BaseModel):
    """Validated chart request model"""
    chart_type: str
    institutions: List[str]
    start_period: str
    end_period: str
    benchmark_type: Optional[str] = "peer_group"
    
    @validator('chart_type')
    def validate_chart_type(cls, v):
        valid_types = ['npl_evolution', 'roe_decomposition', 'capital_ratios']
        if v not in valid_types:
            raise ValueError(f'Invalid chart type. Must be one of: {valid_types}')
        return v
    
    @validator('institutions')
    def validate_institutions(cls, v):
        if len(v) == 0:
            raise ValueError('At least one institution must be selected')
        if len(v) > 20:
            raise ValueError('Maximum 20 institutions allowed')
        return v
    
    @validator('start_period', 'end_period')
    def validate_period_format(cls, v):
        import re
        if not re.match(r'^\d{4}Q[1-4]$', v):
            raise ValueError('Period must be in format YYYYQQ (e.g., 2024Q1)')
        return v
    
    @validator('end_period')
    def validate_period_range(cls, v, values):
        if 'start_period' in values:
            start_year = int(values['start_period'][:4])
            end_year = int(v[:4])
            if end_year - start_year > 10:
                raise ValueError('Maximum 10 years of data allowed')
        return v

# Sanitize chart output
def sanitize_chart_data(chart_data: dict) -> dict:
    """Remove potentially sensitive information from chart data"""
    
    # Remove SQL queries or internal IDs from metadata
    if 'metadata' in chart_data:
        sensitive_keys = ['query', 'internal_id', 'source_table']
        for key in sensitive_keys:
            chart_data['metadata'].pop(key, None)
    
    # Limit precision of financial values
    if 'data' in chart_data:
        for trace in chart_data['data']:
            if 'y' in trace and isinstance(trace['y'], list):
                trace['y'] = [round(val, 2) if isinstance(val, float) else val for val in trace['y']]
    
    return chart_data
```

---

## Conclusion

This technical specification provides a comprehensive framework for implementing Plotly-based interactive visualizations in Banco Insights 2.0. The specification covers:

1. **Detailed chart configurations** for all three TIER 1 dashboards
2. **Interactive features** including hover, click, and selection behaviors
3. **Cross-chart interactivity** for synchronized filtering and linked selections
4. **Data structure requirements** optimized for both frontend rendering and API efficiency
5. **Performance optimization strategies** for handling large Brazilian banking datasets
6. **Professional export capabilities** for investment reports and presentations
7. **Responsive design patterns** ensuring optimal experience across devices
8. **Security and compliance considerations** for financial data visualization

The specification is designed to work seamlessly across both the current Streamlit implementation (v1.0) and the planned React frontend (v2.0), ensuring smooth migration and consistent user experience.

### Key Implementation Benefits:
- **Cross-platform compatibility**: Same chart configurations work in both Streamlit and React
- **Performance optimized**: Handles 12+ years of quarterly data for 2,000+ institutions
- **Professional grade**: Export-ready visualizations for investment reports
- **Interactive insights**: Drill-down capabilities and peer benchmarking
- **Regulatory compliant**: Access control and data privacy built-in

### Next Steps:
1. Implement core chart generation functions following the specifications
2. Set up API endpoints with proper data validation and access control
3. Create React components using the provided integration patterns
4. Implement caching and performance optimization strategies
5. Add comprehensive testing coverage for all chart types

This specification serves as the foundation for building world-class financial data visualizations that meet the demanding requirements of Brazilian banking sector analysis.