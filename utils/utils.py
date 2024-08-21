import json


def string_to_json(input_string: str):
    """Convert a string to JSON if possible."""
    try:
        return json.loads(input_string)
    except json.JSONDecodeError:
        return input_string
