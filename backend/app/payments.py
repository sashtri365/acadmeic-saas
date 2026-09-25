import hashlib
import hmac
from dataclasses import dataclass
from typing import Protocol


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def validate_idempotency_key(key: str) -> str:
    normalized = key.strip()
    if not normalized or len(normalized) > 160:
        raise ValueError("a non-empty idempotency key is required")
    return normalized


class PaymentGateway(Protocol):
    async def create_payment(self, amount: int, currency: str, idempotency_key: str) -> str: ...

    async def refund_payment(self, provider_payment_id: str, amount: int) -> str: ...


@dataclass(frozen=True)
class GatewayPaymentRequest:
    amount_minor: int
    currency: str
    idempotency_key: str


def build_gateway_request(
    amount_minor: int, currency: str, idempotency_key: str
) -> GatewayPaymentRequest:
    """Gateway लाई पैसा पठाउँदा minor unit मात्र प्रयोग गर्नुहोस्।

    नेपाली नोट: Stripe/Razorpay/eSewa/Khalti adapter यही interface मा राख्ने हो।
    Card नम्बर, CVV वा bank account कहिल्यै backendमा नल्याउने; PSP-hosted checkout
    बाट आएको provider token/reference मात्र `payments.provider_token` मा राख्ने।
    """
    if amount_minor <= 0 or len(currency) != 3:
        raise ValueError("amount and ISO currency are required")
    return GatewayPaymentRequest(
        amount_minor, currency.upper(), validate_idempotency_key(idempotency_key)
    )
