# Banco Insights 2.0 — Codebase Overview

**Purpose**
- **Goal:** Banking intelligence platform for Brazil using BACEN IF.data to deliver market insights, benchmarks, and visualizations.
- **Audience:** Investment banking, asset management, strategy teams, and analysts needing Brazilian banking sector analytics.
- **Data Horizon:** 2,000+ institutions, 2013–2024 quarterly data, 700+ metrics (per EDA/docs).

**High-Level Architecture**
- **Frontend:** `frontend/` Next.js 14 + TypeScript + Tailwind + Plotly.js; pages scaffolded with mock data; one chart integrates the backend.
- **Backend:** `backend/` FastAPI serving data and Plotly figure JSON, loading CSVs produced by v1 project.
- **Data & Legacy (v1):** `bacen_project_v1/` ETL, plotting, and large consolidated CSVs used by the backend.
- **EDA:** `EDA/` notebooks and outputs that characterize datasets, columns, and identifiers to guide V2 schema and APIs.

**Repository Structure**
- `backend/`: FastAPI app, endpoints for health, metrics list, institutions, and market-share plot JSON. Reads from `../bacen_project_v1/data/`.
- `frontend/`: Next.js app (static export enabled) with pages for Home, Market Overview, Institution Search, Rankings, Analysis Tools.
- `bacen_project_v1/`: v1 code and data (ETL, plotting, consolidated CSVs). Backend imports plotting from here.
- `EDA/`: EDA README, notebooks, and generated data dictionary/column summaries.
- Root docs: `project-roadmap.md`, `project-scope-briefing.md`, `feature_requirements_prioritization.md` (vision, phased roadmap, prioritized features), plus prompts and planning notes.

**Backend (FastAPI)**
- **Entrypoint:** `backend/main.py`
- **CORS:** Allows `http://localhost:3000` and `http://localhost:3001`.
- **Data Loading:** On startup, loads CSVs from `bacen_project_v1/data`: `market_metrics.csv`, `credit_data.csv`, `financial_metrics_processed.csv`, `financial_metrics.csv`.
- **Plotting Dependency:** Imports `plot_market_share` from `bacen_project_v1/scripts/plotting.py` and returns Plotly figure JSON.
- **Endpoints:**
  - `GET /` and `GET /health`: status
  - `GET /api/metrics`: returns curated list of available metrics
  - `GET /api/institutions`: returns institutions from loaded market dataset
  - `GET /api/market-share`: parameters `feature`, `top_n`, `initial_year`, `drop_nubank`, `custom_selected_institutions[]`; returns `figure_json` (Plotly)
- **Run:** `uvicorn main:app --reload` (defaults to port 8000)

**Frontend (Next.js 14)**
- **Tech:** TypeScript, Tailwind, Plotly via `react-plotly.js`, Lucide icons.
- **Export:** `next.config.js` set to `output: 'export'` for static export; `images.unoptimized: true`.
- **Key Pages:**
  - `/` (Landing): marketing-style overview with mock KPIs
  - `/market-overview`: uses `MarketShareChart` which calls backend for metrics and market-share figure
  - `/institution-search`, `/rankings`, `/analysis-tools`: currently mock data scaffolds with UI components
- **Chart Integration:** `src/components/charts/MarketShareChart.tsx` fetches `GET /api/metrics` and `GET /api/market-share`; dynamic import of Plot to avoid SSR.
- **API Base:** Currently hardcoded to `http://127.0.0.1:8001` (see gaps below).

**EDA**
- **Focus:** Data structure, identifiers (`CodInst`, `NomeInstituicao`, `AnoMes`, `TipoInstituicao`), categorical analysis, data dictionary and columns summary.
- **Outputs:** `banco_insights_data_dictionary.json`, `banco_insights_columns_summary.csv` in `EDA/` to inform DB schema and API.

**Legacy v1**
- **Docs:** `bacen_project_v1/README.md` outlines objective, features, data pipeline, and architecture.
- **ETL:** `bacen_project_v1/scripts/etl.py` and `fetch_data.py` for BACEN IF.data ingestion and consolidation (not read in detail here; serves as current data source).
- **Plotting:** `scripts/plotting.py` and `plotting_financial_waterfall.py` provide Plotly chart generators used by the v2 backend.
- **Data:** Large consolidated CSVs in `bacen_project_v1/data/` used by v2 API.

**What’s Implemented**
- **Backend:**
  - Dataframes load at startup from v1 CSVs.
  - `GET /api/metrics`, `GET /api/institutions`, `GET /api/market-share` operational (assuming data present).
  - Plotly figure JSON returned for market share with customizable parameters incl. special Nubank handling.
- **Frontend:**
  - Complete UI scaffolding with Tailwind styles and components (cards, tables, charts).
  - Landing, Market Overview, Rankings, Institution Search, and Analysis Tools pages with mock data and polished layout.
  - Market Share chart wired to backend endpoints for live figure JSON (base URL hardcoded).
- **Docs & Planning:** Detailed roadmap, scope brief, EDA README, and prioritized feature plan across MVP → V1.1 → V1.2+.

**Gaps & Issues to Address**
- **Port mismatch:** Frontend calls `127.0.0.1:8001` while backend README/run examples use `:8000`. Align via env/config.
- **API base URL hardcoded:** No environment-based configuration for API base; needs `.env` or config layer.
- **Data source coupling:** Backend reads large CSVs directly; roadmap targets Supabase/Postgres. Migration and query layer needed.
- **Limited endpoints:** Only metrics, institutions list, and market-share are exposed; rankings, time series, profiles, and portfolios still mock.
- **Static export vs dynamic data:** `output: 'export'` conflicts with dynamic data fetching for some pages; consider SSR/ISR or client-side fetch strategy per page.
- **CORS origins:** Set to local Next.js ports; will need production origins added.

**Likely Next Steps (from roadmap + code state)**
- **Infra/config**
  - Add shared `.env` and expose `NEXT_PUBLIC_API_BASE_URL`; replace hardcoded URLs in frontend.
  - Align ports (choose 8000 or 8001) and update CORS/README accordingly.
  - Add simple compose/dev scripts to run both apps together.
- **Backend APIs**
  - Add endpoints for: institution profiles, rankings, time series metrics, credit portfolio breakdowns, financial KPIs.
  - Introduce Pydantic models, error handling standardization, and response pagination where applicable.
  - Implement caching for heavy aggregations (e.g., Redis) once DB-backed.
- **Data layer**
  - Design Supabase schema based on EDA outputs; migrate core CSVs to Postgres.
  - Replace CSV reads with SQL queries; add indices and materialized views for common aggregations.
- **Frontend integration**
  - Wire up search, rankings, analysis tools to real endpoints.
  - Add loading/error states consistently and export/download features for charts and tables.
  - Consider ISR/SSR for SEO-critical pages; keep charts client-side.
- **Quality & delivery**
  - Add lint/format/test pipelines; type definitions for API responses.
  - Document runbooks for local/dev/prod; add Dockerfiles and optional compose.
  - Expand API docs at `/docs` and add a top-level backend README section for endpoints/params.

**Quick Run Notes**
- Backend: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8001` (to match current frontend default)
- Frontend: `cd frontend && npm install && npm run dev` then open `http://localhost:3000`
- Data: Ensure `bacen_project_v1/data/*.csv` remain present for the backend to load.

