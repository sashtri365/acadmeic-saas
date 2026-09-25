import pytest
from fastapi import Request
from sqlalchemy.dialects import postgresql

from app.models import Tenant
from app.tenancy import resolve_tenant_context, tenant_query


def make_request(host: str) -> Request:
    scope = {"type": "http", "headers": [(b"host", host.encode())]}
    return Request(scope)


def test_tenant_context_uses_subdomain() -> None:
    context = resolve_tenant_context(make_request("academy.example.com"))

    assert context.subdomain == "academy"
    assert context.hostname == "academy.example.com"


def test_local_tenant_context_defaults_to_demo() -> None:
    assert resolve_tenant_context(make_request("localhost:8000")).subdomain == "demo"


def test_tenant_query_rejects_missing_tenant_id() -> None:
    with pytest.raises(ValueError, match="tenant_id is required"):
        tenant_query(Tenant, None)


def test_tenant_query_contains_tenant_filter() -> None:
    statement = tenant_query(Tenant, "tenant-id")
    compiled = str(statement.compile(dialect=postgresql.dialect()))

    assert "tenants.id" in compiled
    assert "WHERE" in compiled
