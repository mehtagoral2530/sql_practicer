# SQL Healthcare Practice

Interactive SQL lessons for healthcare analytics. Write queries in the browser, run them against PostgreSQL or MySQL, and get teaching-focused feedback when something goes wrong.

## Prerequisites

- **Docker Desktop** (or Docker Engine + Compose) for PostgreSQL and MySQL
- **Python 3.11+** for the FastAPI backend
- **Node.js 20+** and **npm** for the React frontend and Playwright smoke tests

## Quick start

```bash
git clone https://github.com/mehtagoral2530/sql_practicer.git
cd sql_practicer
make install
make up
```

In two terminals:

```bash
# Terminal 1 — API on http://localhost:8000
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — UI on http://localhost:5173
cd frontend && npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The app loads lesson 1 with starter SQL; click **Run** or press **Ctrl+Enter** (Cmd+Enter on macOS).

## Make targets

| Target | Description |
|--------|-------------|
| `make install` | Install Python, frontend, and root (Playwright) dependencies |
| `make up` | Start PostgreSQL (port 5433) and MySQL (port 3307) via Docker |
| `make down` | Stop database containers |
| `make reset` | Recreate databases from seed data (destroys volumes) |
| `make dev` | Print dev-server commands |
| `make test` | `make up`, then backend pytest and frontend vitest |
| `make test-backend` | Run full `pytest` in `backend/` (needs Docker DBs) |
| `make test-backend-unit` | Run backend unit tests without Docker |
| `make test-frontend` | Run `vitest run` in `frontend/` |
| `make validate-lessons` | Run every lesson `solutionSql` on both dialects (requires `make up`) |
| `make smoke` | `make up`, then Playwright end-to-end smoke tests |

## Database connection

Docker Compose seeds the `healthcare` schema on both engines. The backend connects as read-only user `learner_ro` / `learner`:

| Engine | Host | Port | Database |
|--------|------|------|----------|
| PostgreSQL | `localhost` | `5433` | `healthcare` |
| MySQL | `localhost` | `3307` | `healthcare` |

Override with environment variables (`PG_HOST`, `PG_PORT`, `MYSQL_HOST`, etc.) if needed.

## Project layout

```
backend/          FastAPI API, SQL executor, lesson validation
frontend/         React + CodeMirror UI
lessons/          25 JSON lesson files + manifest.json
db/               Init scripts and seed data
e2e/              Playwright smoke tests
```

## Running tests

**Backend unit tests** (no Docker required):

```bash
make test-backend-unit
```

**Backend integration tests** (databases must be up):

```bash
make up
make test-backend
```

**Frontend** (Vitest + Testing Library):

```bash
make test-frontend
```

**All automated tests** (backend + frontend + lesson validator):

```bash
make test
```

**Lesson solution validator** (CI-friendly check that every official answer runs):

```bash
make up
make validate-lessons
# or: cd backend && python3 scripts/validate_lessons.py
```

**End-to-end smoke** (starts backend + frontend via Playwright, runs browser tests):

```bash
make install
make smoke
```

First smoke run may download Playwright browsers:

```bash
npx playwright install chromium
```

## Manual verification checklist

Use this after setup or before a release:

- [ ] `make up` — both DB containers healthy (`docker compose ps`)
- [ ] `curl http://localhost:8000/api/health` — `postgres` and `mysql` are `true` (with dev servers running)
- [ ] Open UI — title **SQL Healthcare Practice**, lesson dropdown populated
- [ ] Run lesson 1 on PostgreSQL — results table appears, lesson passes
- [ ] Switch dialect to MySQL — run again, results appear
- [ ] Introduce typo `FRMO` — error panel shows line number and fix hint
- [ ] `make test-backend-unit` — unit tests pass without Docker
- [ ] `make test-backend` — all pytest tests pass (with Docker)
- [ ] `make test-frontend` — all vitest tests pass
- [ ] `make validate-lessons` — 25 lessons × 2 dialects OK
- [ ] `make smoke` — 3 Playwright tests pass

## Lessons

25 lessons across five modules (SELECT, filter & sort, aggregates, joins, subqueries). Content lives in `lessons/`; the manifest is `lessons/manifest.json`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All changes go through GitHub issues and pull requests.

## License

See repository settings on GitHub.
