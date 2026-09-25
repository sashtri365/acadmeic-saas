
# CampusOS

Tenant-aware academic operations SaaS built from the project blueprint in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

The repository is prepared for cloud deployment. Cloud-specific work still required: provision PostgreSQL/Redis, configure secret environment variables, run the migration job, attach domains/TLS, and deploy the two container images.

## Local development

### Frontend

```powershell
npm ci
Copy-Item .env.example .env.local
npm run dev
```

Frontend: `http://localhost:3000`

### Backend

```powershell
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
pytest
ruff check .
black --check .
uvicorn app.main:app --reload
```

Backend health: `http://localhost:8000/health`

### Full local stack

```powershell
docker compose up --build
```

This starts the frontend, backend, PostgreSQL, and Redis. The credentials in `compose.yaml` are local-only development values and must never be reused in cloud environments.

## Validation

CI runs these gates on every push and pull request:

- Frontend: `npm ci`, ESLint, TypeScript, production build
- Backend: Ruff, Black, pytest, offline Alembic migration rendering

Run the same checks locally before pushing.

## Cloud handoff

1. Build and publish the root frontend image and `backend/` image to the cloud container registry.
2. Provision managed PostgreSQL and Redis on private networking where possible.
3. Configure backend secrets through the cloud secret manager, never through Git: `DATABASE_URL`, `ALLOWED_HOSTS`, `CORS_ORIGINS`, and future auth/session signing secrets.
4. Run `alembic upgrade head` as a one-off migration job before changing application traffic.
5. Deploy the backend on port `8000` and frontend on port `3000` behind the provider's TLS/reverse proxy.
6. Configure `NEXT_PUBLIC_API_BASE_URL` to the backend HTTPS origin and point institution subdomains to the frontend.
7. Verify `/health`, login, tenant resolution, and rollback to the previous image if checks fail.

The application intentionally does not contain provider-specific deployment credentials or cloud account configuration.

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
