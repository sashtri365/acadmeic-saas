# CampusOS Backend

Phase 0 provides the FastAPI application factory, environment settings, and a health endpoint.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
ruff check .
black --check .
alembic check
uvicorn app.main:app --reload
```

Health check: `GET http://localhost:8000/health`

The backend does not yet authenticate users or access a database. Those behaviors begin in later blueprint phases.