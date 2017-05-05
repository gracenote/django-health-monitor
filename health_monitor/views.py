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

import json

from django.http import HttpResponse
try:
    from django.views import View
except ImportError:
    from django.views.generic import View

from . import utils
from .models import HealthTest


class HealthView(View):
    def get(self, request, uid=None, group=None, test=None):
        """Get health by uid, group, and/or test."""
        status_code = 200
        if not test and not group and not uid:
            response_data = {
                'uids': [x.uid for x in self.health_model.objects.all()],
            }
        else:
            try:
                health = self.health_model.objects.get(uid=uid)
                if test and group:
                    state = {k: {x: y for x, y in v.items() if x == test} for k, v in health.state.items() if k == group}
                    severity = {k: v for k, v in health.severity.items() if k == group}
                elif group:
                    state = {k: v for k, v in health.state.items() if k == group}
                    severity = {k: v for k, v in health.severity.items() if k == group}
                else:
                    state = health.state
                    severity = health.severity
                response_data = {
                    'uid': health.uid,
                    'state': state,
                    'severity': severity,
                }
            except Exception as e:
                response_data = {
                    'uid': uid,
                    'message': str(e)
                }
                status_code = 400
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)

    def delete(self, request, uid=None, group=None, test=None):
        """Delete health by uid, group, and/or test."""
        status_code = 200
        try:
            if not test and not group:
                self.health_model.objects.get(uid=uid).delete()
                response_data = {
                    'message': '{} health deleted'.format(uid)
                }
            elif not test:
                self.health_model.objects.get(uid=uid).delete_group(group)
                response_data = {
                    'message': '{} group deleted from {} health'.format(group, uid)
                }
            else:
                self.health_model.objects.get(uid=uid).delete_group_test(group, test)
                response_data = {
                    'message': '{} test deleted from {} group in {} health'.format(test, group, uid)
                }
        except Exception as e:
            response_data = {
                'message': str(e)
            }
            status_code = 400
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)


class HealthAlarmView(View):
    def get(self, request, group=None, test=None):
        status_code = 200
        try:
            if not group:
                raise Exception('group required')
            elif not test:
                response_data = {'tests': HealthTest._get_tests(group)}
            else:
                kwargs = {}
                for k in ['score', 'aggregate_percent', 'repetition', 'repetition_percent']:
                    if k in request.GET.keys():
                        kwargs[k] = int(request.GET[k])
                response_data = self.health_alarm_model.calculate_alarms(group=group, test=test, **kwargs)
        except Exception as e:
                response_data = {
                    'message': str(e)
                }
                status_code = 400

        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)


class HealthTestView(View):
    def get(self, request, uid=None, test=None):
        """Get historical test results by test, uid."""
        status_code = 200
        try:
            if not uid and not test:
                response_data = {'tests': HealthTest._get_tests()}
            else:
                model = HealthTest._get_model(test)
                kwargs = {}
                if uid:
                    kwargs['uids'] = [uid]
                elif 'uids' in request.GET:
                    kwargs['uids'] = request.GET['uids'].split(',')
                if 'start_time' in request.GET:
                    kwargs['start_time'] = utils.iso_to_datetime(request.GET['start_time'])
                if 'end_time' in request.GET:
                    kwargs['end_time'] = utils.iso_to_datetime(request.GET['end_time'])

                response_data = []
                fields = [x.name for x in model._meta.fields if x.name != 'id']
                for result in model.get_history(**kwargs):
                    entry = {}
                    for field in fields:
                        entry[field] = utils.datetime_to_iso(getattr(result, field))
                        entry['score'] = result.get_score()
                    response_data.append(entry)
        except Exception as e:
                response_data = {
                    'message': str(e)
                }
                status_code = 400

        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)

    def post(self, request, uid=None, test=None):
        """Post health test by test and uid."""
        kwargs = {}
        response_data = {}

        if request.POST:
            for key, value in request.POST.items():
                kwargs[key] = value

        # calculate health score: red, orange, yellow, green
        try:
            model = HealthTest._get_model(test)
            kwargs = utils.clean_str_to_bool(model, **kwargs)
            result = model.create(uid=uid, **kwargs)
        except Exception as e:
            response_data['message'] = str(e)
            status_code = 400
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)

        score = result.get_score()
        response_data['score'] = score
        response_data['message'] = '{} score changed to {} for uid {}'.format(test, score, uid)

        return HttpResponse(json.dumps(response_data), content_type="application/json")
