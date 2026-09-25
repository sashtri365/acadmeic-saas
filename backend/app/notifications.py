import re

SENSITIVE_MARKERS = re.compile(
    r"\b(?:marks?|score|grade|gpa|dob|date of birth|citizenship|password)\b", re.IGNORECASE
)


def safe_notification_body(body: str, sensitive: bool = False) -> str:
    if sensitive or SENSITIVE_MARKERS.search(body):
        return "You have a new private update. Tap to view it securely."
    return body[:1000]
