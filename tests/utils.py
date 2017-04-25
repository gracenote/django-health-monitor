import json


def get_content_dict(c):
    """Convert response.content to a dictionary."""
    try:
        return json.loads(c)
    except Exception:
        return json.loads(str(c, 'utf-8'))
