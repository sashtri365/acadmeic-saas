from uuid import uuid4

from app.audit import dashboard_scope, redact_audit_metadata


def test_audit_metadata_redacts_security_values() -> None:
    data = redact_audit_metadata({"action": "role.change", "password": "secret", "token": "jwt"})

    assert data["action"] == "role.change"
    assert data["password"] == "[REDACTED]"
    assert data["token"] == "[REDACTED]"


def test_dashboard_scope_always_contains_tenant_and_user() -> None:
    tenant_id, user_id = uuid4(), uuid4()

    assert dashboard_scope(tenant_id, user_id, "teacher") == {
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "role": "teacher",
    }
