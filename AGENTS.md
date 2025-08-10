# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: FastAPI service (`main.py`), deps in `requirements.txt`; reads CSVs from `bacen_project_v1/data/`.
- `frontend/`: Next.js 14 + TypeScript app (`src/` for pages/components, Tailwind config present).
- `bacen_project_v1/`: Legacy data and scripts; primary CSV assets live in `data/`.
- `EDA/`: Notebooks and exploratory docs.

## Build, Test, and Development Commands
- Backend (from `backend/`):
  - `pip install -r requirements.txt`: install deps.
  - `uvicorn main:app --reload --port 8000`: run API locally.
  - `python main.py`: alternative dev run.
- Frontend (from `frontend/`):
  - `npm install`: install deps (Node 18+).
  - `npm run dev`: start Next.js at `http://localhost:3000`.
  - `npm run build && npm start`: production build/serve.
  - `npm run lint` or `npm run dev:safe`: lint (and run dev if clean).

## Coding Style & Naming Conventions
- Python (backend): PEP 8, 4-space indent, snake_case for functions/variables, PascalCase for classes. Keep FastAPI routers, models, and utils modular when added.
- TypeScript/React (frontend): follow ESLint `next/core-web-vitals`; prefer functional components, PascalCase for components, camelCase for props/state, kebab-case for filenames under `styles/`.
- Paths: refer to data via `backend/../bacen_project_v1/data/*.csv` (see `backend/main.py`). Avoid hardcoding absolute paths.

## Testing Guidelines
- Current: no formal test suites in repo.
- Recommended:
  - Backend: `pytest` with API tests via `httpx` or `fastapi.testclient`; aim for key endpoint coverage (`/api/*`).
  - Frontend: Jest + React Testing Library for components and pages.
- Place tests under `backend/tests/` and `frontend/src/__tests__/`. Name tests `test_*.py` (Python) and `*.test.tsx` (TS).

## Commit & Pull Request Guidelines
- Commits: write clear, scoped messages. Conventional style is encouraged (e.g., `feat:`, `fix:`, `docs:`). Example: `fix: handle empty institution list in /api/market-share`.
- PRs: include purpose, linked issues, setup/run notes, and screenshots for UI changes. Keep PRs focused and small.

## Security & Configuration Tips
- Do not commit secrets or large datasets; use `.gitignore` and local `.env` if needed.
- CORS allows `http://localhost:3000/3001` by default. Update in `backend/main.py` if your dev host differs.
