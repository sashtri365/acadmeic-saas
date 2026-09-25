# CampusOS Backend

The backend provides the FastAPI application factory, secure environment settings, tenant foundation models, and a health endpoint.

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

Health check: `GET http://localhost:8000/health`. Production API documentation is disabled by configuration.

The backend does not yet authenticate users or expose domain APIs. Those behaviors begin in later blueprint phases. Set `DATABASE_URL` through the cloud secret manager before starting a production instance.