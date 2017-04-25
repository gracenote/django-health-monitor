import datetime
import dateutil.parser
import pytz

from django.utils import timezone


def init_score_dict(t, k):
    """Initializes k: {} entry in dict, t if not present."""
    if k not in t.keys():
        t[k] = {'score': None, 'updated': timezone.now()}
    return t


def update_score_dict(t, s):
    """Updates score in dict, and changes update time if value changes."""
    if s != t['score']:
        t['score'] = s
        t['updated'] = timezone.now()
    return t


def datetime_to_iso(t):
    """Converts a datetime object to ISO format string."""
    if isinstance(t, datetime.datetime):
        return t.isoformat()
    return t


def iso_to_datetime(t):
    """Converts an ISO format string to a datetime object with UTC timezone."""
    t = t.replace(' ', '+')
    try:
        return dateutil.parser.parse(t).astimezone(tz=pytz.UTC)
    except Exception:
        return dateutil.parser.parse(t)
