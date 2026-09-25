import hashlib

from fastapi import Request

from .config import get_settings


def client_key(request: Request, tenant: str) -> str:
    address = request.client.host if request.client else "unknown"
    digest = hashlib.sha256(address.encode()).hexdigest()[:24]
    return f"login:{tenant}:{digest}"


async def allow_login_attempt(request: Request, tenant: str) -> bool:
    """Redis fixed-window limiter; production must use shared Redis, not process memory."""
    settings = get_settings()
    if not settings.redis_url:
        return settings.environment != "production"

    try:
        from redis.asyncio import Redis

        redis = Redis.from_url(settings.redis_url, decode_responses=True)
        key = client_key(request, tenant)
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, settings.login_rate_window_seconds)
        await redis.aclose()
        return count <= settings.login_rate_limit
    except Exception:
        # Production fails closed when the shared limiter is unavailable.
        return settings.environment != "production"
