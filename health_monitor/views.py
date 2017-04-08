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

# Import user-defined configuration files declared in settings.py
import sys

from django.conf import settings
sys.path.append(settings.HEALTH_MONITOR_CONFIG)

try:
    from dispatcher import get_dispatcher
except ImportError as e:
    raise ImportError(e)


"""Imports needed for generic views:

health/read/
health/update/
"""

import datetime
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from health_monitor import scoring_helper
from health_monitor.models import Health

try:
    from django.db.models.loading import get_model
except ImportError:
    from django.apps import apps
    get_model = apps.get_model


"""Generic Views

health/<uid>/read/
health/<uid>/update/
health/<uid>/history/<group>/?start_time=<start_time>&end_time=<end_time>
"""


@method_decorator(csrf_exempt, name='dispatch')
class HealthView(View):
    def get(self, request, uid=None, group=None, test_name=None):
        """"""
        if not uid:
            response_data = {
                'uids': [x.uid for x in Health.objects.all()],
                'status': 'success'
            }
        else:
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

    def post(self, request, uid=None, group=None, test_name=None):
        """Generic view to update health for a single UID."""
        kwargs = {}
        response_data = {}

        if request.POST:
            for key, value in request.POST.items():
                kwargs[key] = value

        # calculate health score: red, orange, yellow, green
        try:
            score = scoring_helper.get_score(test_name, **kwargs)
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

    def delete(self, request, uid=None, group=None, test_name=None):
        if uid and not test_name:
            try:
                Health.objects.get(uid=uid).delete()
                response_data = {
                    'status': 'success',
                    'message': '{} deleted'.format(uid)
                }
            except Exception as e:
                response_data = {
                    'status': 'failure',
                    'message': str(e)
                }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # def history(self, request, uid=None, group=None):
    #     """Generic view to return historical test results.
    #
    #     Time should be passed in url in the format '%Y-%m-%d %H:%M:%S'
    #     Default start_time is two hours in the past.
    #     Default end_time is now.
    #     """
    #     start_time = request.GET['start_time'] if 'start_time' in request.GET.keys() else datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    #     end_time = request.GET['end_time'] if 'end_time' in request.GET.keys() else datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    #
    #     response_data = {}
    #     dispatcher = get_dispatcher()
    #     health_keys = health_helper.get_health_keys(group)
    #
    #     for test_name in health_keys:
    #         model = get_model('monitoring', dispatcher[test_name]['model'])
    #         response_data[test_name] = {}
    #         if 'time' in dispatcher[test_name].keys():
    #             timerange = dispatcher[test_name]['time'] + '__range'
    #             model.objects.filter(**{timerange: (start_time, end_time)})
    #         elif 'start_time' in dispatcher[test_name].keys() and 'end_time' in dispatcher[test_name].keys():
    #             start_timerange = dispatcher[test_name]['start_time'] + '__gte'
    #             end_timerange = dispatcher[test_name]['end_time'] + '__lte'
    #             model.objects.filter(**{start_timerange: start_time}).filter(**{end_timerange: end_time})
