from dataclasses import dataclass

from fastapi import Request
from sqlalchemy import Select, select

from .models import Tenant


@dataclass(frozen=True)
class TenantRequestContext:
    subdomain: str
    hostname: str


def resolve_tenant_context(request: Request) -> TenantRequestContext:
    hostname = (request.headers.get("host") or "localhost").split(":", 1)[0].lower()
    parts = hostname.split(".")
    subdomain = parts[0] if len(parts) > 2 and parts[0] not in {"www", "app"} else "demo"
    return TenantRequestContext(subdomain=subdomain, hostname=hostname)


def tenant_query(model: type[Tenant], tenant_id: object | None) -> Select[tuple[Tenant]]:
    if tenant_id is None:
        raise ValueError("tenant_id is required for tenant-scoped queries")
    return select(model).where(model.id == tenant_id)
