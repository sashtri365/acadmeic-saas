import hashlib
import hmac

import pytest

from app.payments import build_gateway_request, validate_idempotency_key, verify_webhook_signature


def test_webhook_signature_requires_exact_provider_signature() -> None:
    payload = b'{"event":"payment.succeeded"}'
    secret = "provider-secret"
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    assert verify_webhook_signature(payload, signature, secret)
    assert not verify_webhook_signature(payload, "bad", secret)


def test_idempotency_key_is_required_and_bounded() -> None:
    assert validate_idempotency_key(" invoice-123 ") == "invoice-123"
    with pytest.raises(ValueError):
        validate_idempotency_key("")
    with pytest.raises(ValueError):
        validate_idempotency_key("x" * 161)


def test_gateway_request_uses_minor_units_and_normalizes_currency() -> None:
    request = build_gateway_request(1250, "npr", "invoice-1")

    assert request.amount_minor == 1250
    assert request.currency == "NPR"
