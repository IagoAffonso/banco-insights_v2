# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Banco Insights 2.0 is a Brazilian banking sector intelligence platform that provides market analysis and benchmarks for 2,000+ financial institutions regulated by BACEN (Central Bank of Brazil). The project currently consists of:

- **v1.0 MVP**: Python-based Streamlit application with FastAPI backend
- **v2.0 Roadmap**: Planned React/Next.js frontend with enhanced FastAPI backend

## Architecture

### Current Structure (v1.0)
- **Data Layer**: BACEN IFDATA API integration, CSV files, Google Cloud Storage
- **Backend**: FastAPI (`api/simple.py`) with plotting utilities (`scripts/`)
- **Frontend**: Streamlit multi-page application (`streamlit_app/`)
- **ETL**: Python scripts for data fetching and processing (`scripts/etl.py`, `scripts/fetch_data.py`)
- **Deployment**: Google Cloud Platform (Cloud Run)

### Key Components
- **Data Sources**: 12+ years of quarterly BACEN data (2013-2024)
- **Analytics**: Market share, credit portfolios, financial statements (DRE), time series
- **Coverage**: Individual institution analysis, sector-wide trends

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r bacen_project_v1/requirements.txt

# Install package in development mode (from bacen_project_v1/)
pip install -e .
```

### Running the Application
```bash
# Start Streamlit frontend
cd bacen_project_v1
streamlit run streamlit_app/Intro.py

# Start FastAPI backend (for API access)
cd bacen_project_v1
uvicorn api.simple:app --reload
```

### Data Management
```bash
# Run ETL pipeline
cd bacen_project_v1
python scripts/etl.py

# Fetch new BACEN data
python scripts/fetch_data.py
```

## Key Files and Directories

### Core Application
- `bacen_project_v1/streamlit_app/Intro.py` - Main Streamlit entry point
- `bacen_project_v1/api/simple.py` - FastAPI backend with GCS integration
- `bacen_project_v1/requirements.txt` - Python dependencies

### Data Processing
- `bacen_project_v1/scripts/fetch_data.py` - BACEN API data fetching
- `bacen_project_v1/scripts/etl.py` - Data transformation pipeline
- `bacen_project_v1/scripts/plotting.py` - Visualization utilities
- `bacen_project_v1/data/` - Local data storage

### Streamlit Pages
- `bacen_project_v1/streamlit_app/pages/1_Market_Share_📊.py` - Market share analysis
- `bacen_project_v1/streamlit_app/pages/2_Share_por_Linha_Crédito💰.py` - Credit segment analysis
- `bacen_project_v1/streamlit_app/pages/3_Carteira_Credito_IFs💳.py` - Credit portfolio analysis
- `bacen_project_v1/streamlit_app/pages/4_DREs📑.py` - Financial statements
- `bacen_project_v1/streamlit_app/pages/5_Series_Temporais_📈.py` - Time series analysis

### Documentation
- `project-roadmap.md` - Comprehensive v2.0 development plan
- `project-scope-briefing.md` - Strategic vision and technical requirements
- `bacen_project_v1/README.md` - Current application overview

## Data Sources and Integration

### BACEN IFDATA API
- **Endpoint**: `https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata`
- **Data Types**: Quarterly financial reports (Tipo2_RelatorioT)
- **Authentication**: Service account credentials (`key.json`)

### Google Cloud Storage
- **Bucket**: Financial data storage and retrieval
- **Integration**: `google-cloud-storage` library in `api/simple.py`

## Development Notes

### Code Patterns
- **Error Handling**: Comprehensive logging in data fetching and API calls
- **Data Processing**: Pandas-heavy operations with CSV file handling
- **Visualization**: Plotly for interactive charts
- **Authentication**: GCP service account for cloud resource access

### Dependencies
- **Core**: FastAPI, Streamlit, pandas, plotly
- **Cloud**: google-cloud-storage, pandas-gbq
- **API**: requests, uvicorn
- **Data**: numpy, python-dateutil

### Future Development (v2.0)
The roadmap indicates migration to:
- **Frontend**: React/Next.js with modern UI/UX
- **Backend**: Enhanced FastAPI with PostgreSQL/Supabase
- **Features**: AI-powered insights, advanced benchmarking, user authentication
- **Infrastructure**: Kubernetes, enhanced GCP deployment