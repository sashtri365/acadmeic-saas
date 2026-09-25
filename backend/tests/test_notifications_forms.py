import pytest

from app.forms import validate_form_schema
from app.notifications import safe_notification_body


def test_sensitive_notification_body_is_tap_to_view() -> None:
    assert "89" not in safe_notification_body("Your marks are 89")
    assert "securely" in safe_notification_body("Personal update", sensitive=True)


def test_form_schema_is_backend_defined_and_validated() -> None:
    schema = {"fields": [{"name": "legal_name", "type": "text"}, {"name": "dob", "type": "date"}]}
    assert validate_form_schema(schema) == schema
    with pytest.raises(ValueError):
        validate_form_schema({"fields": [{"name": "x", "type": "unknown"}]})
    with pytest.raises(ValueError):
        validate_form_schema(
            {"fields": [{"name": "x", "type": "text"}, {"name": "x", "type": "text"}]}
        )
