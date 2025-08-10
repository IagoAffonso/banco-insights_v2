# Banco Insights 2.0 - Backend API

FastAPI backend for the Banco Insights 2.0 platform, providing Brazilian banking sector data analysis and visualization endpoints.

## Features

- **Market Share Analysis**: Interactive stacked area charts with customizable parameters
- **Institution Data**: Complete list of 2000+ Brazilian financial institutions
- **Metrics**: 13+ financial metrics available for analysis
- **Time Series**: Historical data from 2013-2024 (quarterly)

## API Endpoints

### Core Endpoints

- `GET /` - API welcome and status
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### Data Endpoints

- `GET /api/market-share` - Generate market share visualizations
- `GET /api/metrics` - List available financial metrics
- `GET /api/institutions` - List all institutions

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload

# Or run directly
python main.py
```

The API will be available at http://localhost:8000

## Market Share Parameters

The `/api/market-share` endpoint supports the following interactive parameters:

- **feature**: Financial metric to analyze (default: 'Quantidade de clientes com operações ativas')
- **top_n**: Number of top institutions to display (1-50, default: 10)
- **initial_year**: Starting year for analysis (2013-2024, optional)
- **drop_nubank**: Nubank handling (0=keep both, 1=drop NU PAGAMENTOS, 2=drop NUBANK)
- **custom_selected_institutions**: List of specific institutions to include

## Development

### Running the API

```bash
# Development with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## Data Source

The API uses data from the existing v1 project located in `../bacen_project_v1/data/`:

- `market_metrics.csv` - Main market share data
- `credit_data.csv` - Credit portfolio data  
- `financial_metrics_processed.csv` - Processed financial metrics
- `financial_metrics.csv` - Raw financial metrics

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000 (Next.js default)
- http://localhost:3001 (Next.js alternative)

Additional origins can be added in the CORS middleware configuration.