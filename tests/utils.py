import json


def content_to_json(c):
    try:
        return c.json()
    except Exception:
        return json.loads(c.decode('utf8'))
