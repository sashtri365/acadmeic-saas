from uuid import uuid4

import pytest

from app.config import get_settings
from app.rbac import AuthenticatedUser, require_permission, require_scope
from app.security import create_access_token, decode_access_token, hash_password, verify_password


def test_argon2_passwords_verify_without_exposing_plaintext() -> None:
    password_hash = hash_password("correct horse battery staple")

    assert password_hash.startswith("$argon2id$")
    assert verify_password("correct horse battery staple", password_hash)
    assert not verify_password("wrong", password_hash)


def test_access_token_contains_server_issued_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWT_SECRET", "test-only-secret-that-is-at-least-32-bytes")
    get_settings.cache_clear()
    user_id, tenant_id = uuid4(), uuid4()

    token = create_access_token(user_id, tenant_id, ["teacher"])
    payload = decode_access_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["tenant_id"] == str(tenant_id)
    assert payload["roles"] == ["teacher"]


def test_rbac_rejects_wrong_tenant_and_role() -> None:
    user = AuthenticatedUser(uuid4(), uuid4(), frozenset({"teacher"}))

    with pytest.raises(Exception) as role_error:
        require_permission(user, "fees.write", {"institution_admin"})
    assert role_error.value.status_code == 403

    with pytest.raises(Exception) as tenant_error:
        require_scope(user, uuid4())
    assert tenant_error.value.status_code == 403
