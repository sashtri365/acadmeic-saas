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

Authentication, tenant isolation, RBAC, payment security helpers, notification redaction, and audit foundations are implemented. Domain CRUD endpoints and live provider adapters are added phase by phase. Set `DATABASE_URL`, `REDIS_URL`, and `JWT_SECRET` through the cloud secret manager before starting production.

Production security requirements:

- `JWT_SECRET` must be at least 32 characters.
- `SECURE_COOKIES=true` is mandatory.
- `REDIS_URL` is required for shared login rate limiting.
- `ALLOWED_HOSTS` and `CORS_ORIGINS` must be explicit; wildcard values are rejected.