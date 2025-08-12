# Banco Insights 2.0 — Architecture, Improvements, and Deployment Plan

This report summarizes how data flows through the repository, the current backend and frontend integration, and recommends concrete improvements and a production deployment plan that is easy to test locally, deploy on Supabase, and maintain over time.

## Executive Summary

- Data lives in CSVs under `bacen_project_v1/data/` and is loaded by a FastAPI backend (`backend/main.py`).
- The backend exposes REST endpoints that aggregate data and, for market share, returns Plotly figure JSON. CORS is enabled for local Next.js dev.
- The Next.js frontend (`frontend/`) calls the backend using `NEXT_PUBLIC_API_BASE_URL` and renders charts and pages (market overview, rankings, etc.).
- Recommended improvements focus on: robust data loading and schema, API response typing and consistency, better frontend API integration, test coverage, and containerized deployment.
- For production, move data into Supabase (Postgres) with a simple schema, then deploy: frontend on Vercel, backend on a small app host (Render/Fly/Heroku) or Supabase Edge Functions for some read-only APIs. Keep local dev simple with `.env` files and `docker-compose` (optional) for parity.

---

## Current Architecture

### Data Layer
- Location: `bacen_project_v1/data/`
  - Primary CSVs used in backend:
    - `market_metrics.csv` — market share and key metrics
    - `credit_data.csv` — credit portfolio and modalities
    - `financial_metrics.csv` — raw financial statements
    - `financial_metrics_processed.csv` — processed financials
    - Optional: `consolidated_institutions.json` — lightweight roster used to enrich institution search
- Access pattern: Backend loads data into global Pandas DataFrames on startup.
- Pathing: Relative path from `backend/` to `../bacen_project_v1/data/` as per repo guidelines (good for portability).

### Backend (FastAPI)
- Entry: `backend/main.py`
- CORS: defaults to `http://localhost:3000/3001` or `CORS_ORIGINS` env var.
- Data loading: `@app.on_event('startup')` calls `load_data()` and reads all CSVs into globals.
- External dependency: Tries to import `plot_market_share` from `../bacen_project_v1/scripts/plotting`.
- Notable helpers:
  - `FEATURE_NAME_DICT` maps display names → raw CSV identifiers.
  - `_df_for_feature`, `_latest_quarter`, `_latest_quarter_group`, `_shares` provide aggregation utilities.
- Implemented endpoints (selected):
  - `GET /` and `GET /health` — status checks
  - `GET /api/metrics` and `GET /api/metrics/map` — list of metrics and mapping
  - `GET /api/institutions` — list of institutions
  - `GET /api/market-share` — JSON-serialized Plotly figure
  - `GET /api/snapshot` — latest totals, institution count, top-5 concentration
  - `GET /api/market-concentration` — top N concentration summary
  - `GET /api/rankings` — ranked institutions by feature for a given period
  - `GET /api/timeseries` — quarterly series for a feature (market or institution)
  - `GET /api/credit/segments` — segment breakdown and YoY growth
  - `GET /api/financials/dre` — DRE-like aggregation at market/institution scope

### Frontend (Next.js 14 + TS)
- Structure: `frontend/src/` with `pages/`, `components/`, `utils/`, Tailwind config present.
- API integration:
  - `src/utils/api.ts`: `NEXT_PUBLIC_API_BASE_URL` (defaults to `http://127.0.0.1:8001`)
  - Pages use `fetchJson` or `fetch` directly to call backend.
  - `MarketOverviewPage` and `RankingsPage` call `/api/snapshot`, `/api/market-concentration`, `/api/rankings`, `/api/credit/segments`.
  - `MarketShareChart` calls `/api/metrics`, `/api/institutions`, and `/api/market-share` and renders Plotly client-side.

---

## Gaps and Risks

- Data loading:
  - CSVs loaded into memory on startup; no graceful reload/update strategy; potential memory overhead.
  - No explicit schema validation on CSV load; unexpected column changes may break endpoints.
  - Harder to scale horizontally since each instance loads full CSVs.
- API design:
  - Responses are mostly ad-hoc dicts; no Pydantic models to guarantee shape/typing.
  - Error handling is inconsistent; some exceptions bubble up as generic 500s.
  - `MarketShareChart` fetches with `fetch` directly; elsewhere `fetchJson` is used (mixed styles).
- Frontend:
  - Some pages still show mock data (institution search listings, parts of home/rankings insights), which can diverge from API reality.
  - No shared TypeScript types derived from backend responses.
- Testing:
  - No automated tests; refactors and CSV changes risk regressions.
- Deployment:
  - CSV-based backend isn’t ideal for production scale or concurrent access; a database (Supabase) will improve reliability/perf.

---

## Recommended Improvements

### Data & Backend
- Add configuration for data directory
  - Env var: `DATA_DIR` with default to `../bacen_project_v1/data`.
  - Log resolved path on startup; fail fast with clear message if missing.
- Validate and document data schema
  - Define expected columns for each CSV (README + code assertions).
  - On load, validate presence and types for critical columns (`AnoMes_Q`, `NomeInstituicao`, `Saldo`, etc.).
- Replace startup event with lifespan and a simple repository layer
  - Use FastAPI lifespan to load/cold-cache data, and structure access via a `DataRepository` class for testability.
- Add Pydantic response models
  - Define `MetricItem`, `InstitutionItem`, `RankingItem`, `TimeseriesPoint`, etc. to standardize responses.
- Normalize error handling
  - Catch domain errors and return `HTTPException` with helpful messages; avoid leaking stack traces.
- Performance/caching
  - Cache expensive aggregations (market concentration, snapshot) per period/feature in memory for the process lifetime.
  - Consider precomputing common aggregates during startup or as background tasks.

### Frontend
- Centralize API calls through `fetchJson`
  - Update places using `fetch` directly (e.g., `MarketShareChart`) to use `fetchJson` for consistency and error handling.
- Type API responses
  - Create TS interfaces for backend responses in `src/types/api.ts` and use across pages/components.
- Gradually replace mock data
  - Wire `institution-search` to `/api/institutions` and `/api/institutions/search` (already exists) for real results.
- Add SWR/React Query for data fetching
  - Improve UX with request deduplication, caching, retries, and loading states.
- Production config
  - Ensure `NEXT_PUBLIC_API_BASE_URL` points to the deployed backend URL; align CORS accordingly.

### Testing & Tooling
- Backend
  - Add `pytest` with `fastapi.testclient` to cover: health, metrics, institutions, rankings, timeseries, snapshot, and credit endpoints.
  - Fixture tiny CSVs under `backend/tests/fixtures/` to validate parsing and aggregations.
- Frontend
  - Add Jest + React Testing Library for key components (charts can be smoke-tested with dynamic import mocking).
  - Add ESLint/TypeScript checks to CI.
- Dev ergonomics
  - `.env.example` already present; add `backend/.env.example` for `CORS_ORIGINS`, `DATA_DIR`, and (later) `DATABASE_URL`.
  - Add Makefile or simple npm/yarn scripts for common tasks.

---

## Supabase Data Model (Recommended)

Move core CSV content into a small number of tables. This enables scalable queries, indexing, and partial loads.

- `institutions`
  - `id` (uuid or bigint), `name` (text), `cnpj` (text), `type` (text), `region` (text)
  - Index on `lower(name)`, `cnpj`.
- `metrics_observations` (wide CSV content normalized)
  - `period_q` (text, e.g., `2024Q4`)
  - `period_date` (date, optional)
  - `institution_id` (fk → institutions)
  - `institution_name` (text) — keep denormalized for ease of ingestion
  - `metric_key` (text) — e.g., values from `FEATURE_NAME_DICT`
  - `value` (numeric)
  - Indexes: `(metric_key, period_q)`, `(institution_name, period_q)`, `(period_q)`
- `metrics_map`
  - `display_name` (text) ←→ `raw_key` (text) — source of truth for mappings currently in code.

Notes:
- For first migration, you can keep both `institution_name` and join to `institutions` by name; later, backfill `institution_id`.
- Use materialized views for “latest period per metric” and top-N queries if needed for performance.

---

## Local Development & Testing (Simple Path)

1) Backend
- From `backend/`:
  - `pip install -r requirements.txt`
  - `uvicorn main:app --reload --port 8001`
- Optional env in `backend/.env`:
  - `CORS_ORIGINS=http://localhost:3000`
  - `DATA_DIR=../bacen_project_v1/data`

2) Frontend
- From `frontend/`:
  - `npm install`
  - Set `frontend/.env.local` with `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001`
  - `npm run dev`

3) Test manually
- Visit `http://localhost:3000/market-overview` and `http://localhost:3000/rankings`.
- Swagger at `http://localhost:8001/docs` for API exploration.

Optional: `docker-compose` for parity (sample)

```yaml
version: '3.8'
services:
  api:
    build: ./backend
    environment:
      - CORS_ORIGINS=http://localhost:3000
      - DATA_DIR=/app/bacen_project_v1/data
    volumes:
      - ./bacen_project_v1/data:/app/bacen_project_v1/data:ro
    ports:
      - "8001:8001"
    command: uvicorn main:app --host 0.0.0.0 --port 8001

  web:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://api:8001
    ports:
      - "3000:3000"
    command: npm run dev
    depends_on:
      - api
```

---

## Production Deployment (Supabase + Vercel + App Host)

Target goals: easy deploys, scalable reads, and maintainability.

1) Supabase (Postgres)
- Create a project; obtain `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and service role key.
- Create tables (`institutions`, `metrics_observations`, `metrics_map`).
- Ingest CSVs:
  - Use Supabase Studio or `COPY` via SQL to load CSVs into staging tables, then `INSERT INTO` final tables.
  - Backfill `metrics_map` from current `FEATURE_NAME_DICT` for a single source of truth.
- RLS: enable read-only policies for public views if the frontend will read directly; otherwise, keep data private and access via backend using the service key.

2) Backend (Render/Fly/Heroku/Dokku)
- Containerize the FastAPI backend (multi-stage Dockerfile recommended).
- Set env vars:
  - `DATABASE_URL` (Supabase Postgres URL)
  - `CORS_ORIGINS` (include Vercel domain)
- Modify backend to query Supabase instead of CSVs (phase-in approach below). Keep response shapes unchanged to avoid frontend churn.
- Add health checks and logging to stdout/stderr; consider structured logging.

3) Frontend (Vercel)
- Deploy `frontend/` to Vercel.
- Set `NEXT_PUBLIC_API_BASE_URL` to the deployed backend URL.
- Use ISR/SSG where appropriate for mostly-static pages; keep dynamic charts CSR.

4) Observability & Security
- Add Sentry (frontend + backend) for error tracking.
- Configure CORS to only allow your Vercel domain and local dev.
- Add rate limiting (reverse proxy or app middleware) if exposing public APIs.
- Backups for Supabase (built-in) and migration/versioning scripts kept in repo.

---

## Migration Path: CSV → Supabase

Phase 0: Stabilize on CSV
- Add schema validation, response models, and consistent error handling.
- Extract `FEATURE_NAME_DICT` into a small data module or JSON file under `backend/` for reuse later.

Phase 1: Dual-read capability
- Introduce a repository interface `DataRepository` with two concrete implementations:
  - `CsvRepository` (current logic)
  - `SqlRepository` (Supabase/Postgres via SQLAlchemy or `asyncpg`)
- Add env toggle `DATA_BACKEND=csv|sql` and `DATABASE_URL`.
- Ensure API responses remain identical.

Phase 2: Cutover
- Default `DATA_BACKEND=sql` in production; keep CSV for local dev and as a fallback.
- Decommission CSVs in runtime once all endpoints are verified.

---

## Suggested Backend Refactor Sketch

- `backend/app.py` or keep `main.py`:
  - Wire lifespan to initialize `repo: DataRepository` and attach to `app.state.repo`.
  - Endpoints call `repo` methods rather than touching global DataFrames.
- `backend/repository.py`:
  - Define interface and two implementations (CSV/SQL).
- `backend/models.py`:
  - Pydantic response schemas for endpoints.
- `backend/settings.py`:
  - Pydantic BaseSettings for env (CORS_ORIGINS, DATA_DIR, DATABASE_URL, DATA_BACKEND).

This keeps changes modular, testable, and incremental.

---

## CI/CD and Maintenance

- CI (GitHub Actions)
  - Lint + type-check frontend and backend.
  - Run backend unit tests.
  - Optionally build Docker images to ensure Dockerfile correctness.
- Versioning & Releases
  - Tag releases and attach environment diffs (e.g., changes to `FEATURE_NAME_DICT`).
- Docs
  - Keep `backend/README.md` and `frontend/README.md` up to date; document required env vars clearly.
- Housekeeping
  - Pre-commit hooks for black/ruff/isort (backend) and eslint/prettier (frontend).
  - Avoid committing large datasets; keep `.gitignore` current.

---

## Quick Checklist

- Backend
  - Add `DATA_DIR`, `DATA_BACKEND`, `DATABASE_URL` envs (example file).
  - Pydantic response models; unify errors and logging.
  - Repository abstraction to support CSV and SQL backends.
  - Basic pytest suite covering key endpoints.
- Frontend
  - Use `fetchJson` everywhere; add TS types for responses.
  - Replace mock data where API exists; keep UI skeletons.
  - Confirm `NEXT_PUBLIC_API_BASE_URL` in Vercel.
- Supabase
  - Create tables, load CSVs, index hot paths.
  - Optional: materialized views for “latest period” and top-N.
  - RLS strategy (public read views or backend-only access).
- Deployment
  - Frontend on Vercel; backend on Render/Fly/Heroku with proper CORS.
  - Add health checks and minimal observability (logs, Sentry).

With these steps, the project becomes easy to run locally, straightforward to deploy (with clear envs and hosts), and maintainable as the data and features grow.

