import datetime
import dateutil.parser
import pytz

from django.utils import timezone


def init_score_dict(d, k):
    """Initializes k: {} entry in dict, d if not present."""
    if k not in d.keys():
        d[k] = {'score': None, 'updated': timezone.now()}
    return d


def update_score_dict(d, s):
    """Updates score in dict, and changes update time if value changes."""
    if s != d['score']:
        d['score'] = s
        d['updated'] = timezone.now()
    return d


def datetime_to_iso(d):
    """Converts a datetime object to ISO format string."""
    if isinstance(d, datetime.datetime):
        return d.isoformat()
    return d


def iso_to_datetime(d):
    """Converts an ISO format string to a datetime object with UTC timezone."""
    return dateutil.parser.parse(d).replace(tzinfo=pytz.UTC)
