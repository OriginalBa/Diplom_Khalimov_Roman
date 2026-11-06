FIO_JSON_SCHEMA = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["value", "surname", "name", "second_name", "qc", "sex", "id"],
                "properties": {
                    "value": {"type": "string"},
                    "surname": {"type": "string"},
                    "name": {"type": "string"},
                    "second_name": {"type": "string"},
                    "qc": {"type": "string"},
                    "sex": {"type": "string", "enum": ["man", "woman", ""]},
                    "id": {"type": "string", "minLength": 32, "maxLength": 32}
                }
            }
        }
    }
}

EMAIL_JSON_SCHEMA = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["value", "id"],
                "properties": {
                    "value": {"type": "string"},
                    "id": {"type": "string", "minLength": 32, "maxLength": 32}
                }
            }
        }
    }
}