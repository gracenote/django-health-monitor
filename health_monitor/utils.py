import datetime

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


def iso_format_datetime(d):
    if isinstance(d, datetime):
        return d.isoformat()
    return d
