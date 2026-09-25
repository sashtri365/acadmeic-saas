from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException, status


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: UUID
    tenant_id: UUID
    roles: frozenset[str]


def require_permission(user: AuthenticatedUser, permission: str, allowed_roles: set[str]) -> None:
    if not user.roles.intersection(allowed_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permission")


def require_scope(
    user: AuthenticatedUser,
    tenant_id: UUID,
    resource_scope: str | None = None,
    allowed_scopes: set[str] | None = None,
) -> None:
    if user.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant scope violation")
    if allowed_scopes is not None and resource_scope not in allowed_scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Resource scope violation"
        )


def can_edit_assignment(
    user: AuthenticatedUser,
    assignment_teacher_id: UUID,
    assignment_scope: str,
    requested_scope: str,
) -> bool:
    return user.user_id == assignment_teacher_id and assignment_scope == requested_scope


def can_read_conversation(
    user: AuthenticatedUser, participant_user_ids: set[UUID], tenant_id: UUID
) -> bool:
    return user.tenant_id == tenant_id and user.user_id in participant_user_ids
