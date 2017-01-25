"""Import user-defined configuration files declared in settings.py"""
import sys

from django.conf import settings
sys.path.append(settings.HEALTH_MONITOR_CONFIG)

try:
    from dispatcher import get_dispatcher
except ImportError as e:
    raise ImportError('settings.HEALTH_MONITOR_CONFIG not properly set. See docs at https://django-health-monitor.readthedocs.io/en/latest/usage.html#configure-scoring-logic')


"""Imports needed for generic views:

health/read/
health/update/
"""
import datetime
import json

from django.http import HttpResponse
from health_monitor import health_helper
from health_monitor.models import Health

try:
    from django.db.models.loading import get_model
except ImportError:
    from django.apps import apps
    get_model = apps.get_model


"""Generic Views

health/<uid>/read/
health/<uid>/history/<subscriber>/?start_time=<start_time>&end_time=<end_time>
health/<uid>/update/
"""


def read(request, uid):
    """Generic view to read health for a single UID."""
    try:
        health = Health.objects.get(uid=uid)
        response_data = {
            'uid': health.uid,
            'state': health.state,
            'status': 'success',
            'severity': health.severity,
        }
    except Exception as e:
        response_data = {
            'uid': uid,
            'status': 'failure',
            'message': str(e)
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def history(request, uid, subscriber):
    """Generic view to return historical test results.

    Time should be passed in url in the format '%Y-%m-%d %H:%M:%S'
    Default start_time is two hours in the past.
    Default end_time is now.
    """
    start_time = request.GET['start_time'] if 'start_time' in request.GET.keys() else datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = request.GET['end_time'] if 'end_time' in request.GET.keys() else datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    import ipdb
    ipdb.set_trace()

    response_data = {}
    dispatcher = get_dispatcher()
    health_keys = health_helper.get_health_keys(subscriber)

    for test_name in health_keys:
        model = get_model('monitoring', dispatcher[test_name]['model'])
        response_data[test_name] = {}
        if 'time' in dispatcher[test_name].keys():
            timerange = dispatcher[test_name]['time'] + '__range'
            model.objects.filter(**{timerange: (start_time, end_time)})
        elif 'start_time' in dispatcher[test_name].keys() and 'end_time' in dispatcher[test_name].keys():
            start_timerange = dispatcher[test_name]['start_time'] + '__gte'
            end_timerange = dispatcher[test_name]['end_time'] + '__lte'
            model.objects.filter(**{start_timerange: start_time}).filter(**{end_timerange: end_time})


def update(request, uid=None, test_name=None):
    """Generic view to update health for a single UID."""
    kwargs = {}
    response_data = {}

    if request.GET:
        for key, value in request.GET.items():
            kwargs[key] = value

    # calculate health score: red, orange, yellow, green
    try:
        score = health_helper.get_score(test_name, **kwargs)
    except LookupError as e:
        response_data['status'] = 'error'
        response_data['message'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    health = Health.objects.get_or_create(uid=uid)[0]
    health.update_score(test_name=test_name, score=score)

    response_data['status'] = 'success'
    response_data['score'] = score
    response_data['message'] = '{} changed to {} for uid {}'.format(test_name, score, uid)

    return HttpResponse(json.dumps(response_data), content_type="application/json")
