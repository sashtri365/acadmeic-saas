from typing import Any
from uuid import UUID

SENSITIVE_KEYS = {"password", "token", "authorization", "card_number", "account_number"}


def redact_audit_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else value
        for key, value in metadata.items()
    }


def dashboard_scope(tenant_id: UUID, user_id: UUID, role: str) -> dict[str, str]:
    return {"tenant_id": str(tenant_id), "user_id": str(user_id), "role": role}
