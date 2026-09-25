from uuid import UUID

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .config import get_settings
from .db import get_db_session
from .models import Tenant, User
from .rbac import AuthenticatedUser
from .security import create_access_token, decode_access_token, hash_password, verify_password
from .tenancy import resolve_tenant_context

router = APIRouter(prefix="/auth", tags=["authentication"])
bearer = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    tenantSlug: str


class SessionResponse(BaseModel):
    userId: UUID
    displayName: str
    role: str
    tenantSlug: str
    requiresPasswordReset: bool = False


class PasswordResetRequest(BaseModel):
    email: EmailStr
    tenantSlug: str


class PasswordResetComplete(BaseModel):
    email: EmailStr
    password: str
    tenantSlug: str


async def current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> AuthenticatedUser:
    token = credentials.credentials if credentials else request.cookies.get("campus_session")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    try:
        payload = decode_access_token(token)
        return AuthenticatedUser(
            user_id=UUID(payload["sub"]),
            tenant_id=UUID(payload["tenant_id"]),
            roles=frozenset(payload.get("roles", [])),
        )
    except (KeyError, ValueError, jwt.InvalidTokenError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
        ) from error


@router.post("/login", response_model=SessionResponse)
async def login(
    body: LoginRequest,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
) -> SessionResponse:
    tenant_context = resolve_tenant_context(request)
    if body.tenantSlug != tenant_context.subdomain:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    result = await session.execute(
        select(User, Tenant)
        .join(Tenant, User.tenant_id == Tenant.id)
        .options(selectinload(User.roles))
        .where(
            Tenant.subdomain == body.tenantSlug,
            User.email == body.email.lower(),
            User.is_active.is_(True),
        )
    )
    row = result.first()
    if row is None or not verify_password(body.password, row.User.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    roles = [role.name for role in row.User.roles]
    token = create_access_token(row.User.id, row.Tenant.id, roles)
    settings = get_settings()
    response.set_cookie(
        "campus_session",
        token,
        httponly=True,
        secure=settings.secure_cookies,
        samesite="lax",
        max_age=settings.access_token_minutes * 60,
        path="/",
    )
    return SessionResponse(
        userId=row.User.id,
        displayName=row.User.display_name,
        role=roles[0] if roles else "student_parent",
        tenantSlug=row.Tenant.subdomain,
        requiresPasswordReset=row.User.must_reset_password,
    )


@router.get("/session", response_model=SessionResponse)
async def get_session(
    authenticated_user: AuthenticatedUser = Depends(current_user),
    session: AsyncSession = Depends(get_db_session),
) -> SessionResponse:
    result = await session.execute(
        select(User, Tenant)
        .join(Tenant, User.tenant_id == Tenant.id)
        .options(selectinload(User.roles))
        .where(User.id == authenticated_user.user_id)
    )
    row = result.first()
    if row is None or not row.User.is_active or row.User.tenant_id != authenticated_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    roles = [role.name for role in row.User.roles]
    return SessionResponse(
        userId=row.User.id,
        displayName=row.User.display_name,
        role=roles[0] if roles else "student_parent",
        tenantSlug=row.Tenant.subdomain,
        requiresPasswordReset=row.User.must_reset_password,
    )


@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
async def request_password_reset(_: PasswordResetRequest) -> None:
    # Always return the same response; delivery and token creation belong to the notification phase.
    return None


@router.post("/password-reset/complete", status_code=status.HTTP_204_NO_CONTENT)
async def complete_password_reset(
    body: PasswordResetComplete,
    authenticated_user: AuthenticatedUser = Depends(current_user),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    result = await session.execute(select(User).where(User.id == authenticated_user.user_id))
    user = result.scalar_one_or_none()
    if user is None or user.email != body.email.lower() or not user.must_reset_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Reset is not available"
        )
    user.password_hash = hash_password(body.password)
    user.must_reset_password = False
    await session.commit()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie("campus_session", path="/")
