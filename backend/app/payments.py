import hashlib
import hmac


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def validate_idempotency_key(key: str) -> str:
    normalized = key.strip()
    if not normalized or len(normalized) > 160:
        raise ValueError("a non-empty idempotency key is required")
    return normalized
