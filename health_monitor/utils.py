"""
   Copyright 2017 Gracenote

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from collections import deque
import datetime
import dateutil.parser
import distutils.util
import itertools
import pytz

from django.utils import timezone


def init_score_dict(t, k):
    """Return an initialized dictionary.

    Initialize 'score' and 'updated' keys and values if not present.

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
    """Return a datetime object.

    Return as UTC timezone of an ISO 8601 formatted date string.

    t -- ISO 8601 formatted date string
    """
    t = t.replace(' ', '+')
    try:
        return dateutil.parser.parse(t).astimezone(tz=pytz.UTC)
    except Exception:
        return dateutil.parser.parse(t)


def push_pop_deque(e, l):
    """Return a list with a new element pushed and the oldest element popped.

    The newest element is pushed in the 0 position and oldest element popped
    from the -1 position using deque.

    e -- element
    l -- list
    """
    o = deque(l)
    o.appendleft(e)
    o.pop()
    return list(o)


def clean_str_to_bool(cls, **kwargs):
    """Returns kwargs where any BooleanField is type converted to a bool.

    This issue is caused by request.POST returning '0' for 0, 'False' for
    False, etc., which ends up getting written to the database as a 1 if not
    type converted.
    """
    for k, v in kwargs.items():
        if k in [x.attname for x in cls._meta.fields]:
            if cls._meta.get_field(k).get_internal_type() == 'BooleanField':
                try:
                    kwargs[k] = distutils.util.strtobool(v)
                except Exception as e:
                    error_message = 'BooleanField not type converted in ' \
                        'health_monitor/utils.py - {}'.format(e)
                    raise RuntimeError(error_message)
    return kwargs


def merge_to_uniques(l):
    """Returns a unique list of elements from a list of lists."""
    combined = list(itertools.chain.from_iterable(l))
    return list(set(combined))
