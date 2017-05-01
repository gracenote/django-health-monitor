from collections import deque
import datetime
import dateutil.parser
import pytz

from django.utils import timezone


def init_score_dict(t, k):
    """Return an initialized dictionary with 'score' and 'updated' keys and values if not present.

    Arguments:
    t -- dictionary
    k -- key
    """
    if k not in t.keys():
        t[k] = {'score': None, 'updated': timezone.now()}
    return t


def update_score_dict(t, s):
    """Return a dictionary with updated score and updated time if score changes.

    t -- dictionary
    s -- score
    """
    if s != t['score']:
        t['score'] = s
        t['updated'] = timezone.now()
    return t


def datetime_to_iso(t):
    """Return an ISO 8601 formatted date string of a datetime object.

    t -- datetime object
    """
    if isinstance(t, datetime.datetime):
        return t.isoformat()
    return t


def iso_to_datetime(t):
    """Return a datetime object with UTC timezone of an ISO 8601 formatted date string.

    t -- ISO 8601 formatted date string
    """
    t = t.replace(' ', '+')
    try:
        return dateutil.parser.parse(t).astimezone(tz=pytz.UTC)
    except Exception:
        return dateutil.parser.parse(t)


def push_pop_deque(e, l):
    """Return a list with a new element pushed in the 0 position and oldest element popped from the -1 position using deque.

    e -- element
    l -- list
    """
    o = deque(l)
    o.appendleft(e)
    o.pop()
    return list(o)
