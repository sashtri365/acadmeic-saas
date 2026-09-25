ALLOWED_FIELD_TYPES = {"text", "email", "date", "number", "select", "textarea", "file"}


def validate_form_schema(schema: dict) -> dict:
    fields = schema.get("fields")
    if not isinstance(fields, list) or not fields:
        raise ValueError("form schema requires a non-empty fields list")
    seen: set[str] = set()
    for field in fields:
        if not isinstance(field, dict) or not isinstance(field.get("name"), str):
            raise ValueError("each form field requires a name")
        if field["name"] in seen:
            raise ValueError("form field names must be unique")
        if field.get("type") not in ALLOWED_FIELD_TYPES:
            raise ValueError("unsupported form field type")
        seen.add(field["name"])
    return schema
