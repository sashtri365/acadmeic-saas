from uuid import uuid4

from app.rbac import AuthenticatedUser, can_read_conversation


def test_conversation_visibility_requires_participant_and_tenant() -> None:
    tenant_a, tenant_b = uuid4(), uuid4()
    user = AuthenticatedUser(uuid4(), tenant_a, frozenset({"teacher"}))

    assert can_read_conversation(user, {user.user_id}, tenant_a)
    assert not can_read_conversation(user, {uuid4()}, tenant_a)
    assert not can_read_conversation(user, {user.user_id}, tenant_b)
