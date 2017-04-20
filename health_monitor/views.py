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

from .models import HealthTest


class HealthView(View):
    def get(self, request, uid=None, group=None, test=None):
        """Get health by uid."""
        if not uid:
            response_data = {
                'uids': [x.uid for x in self.health_model.objects.all()],
            }
            status_code = 200
        else:
            try:
                health = self.health_model.objects.get(uid=uid)
                response_data = {
                    'uid': health.uid,
                    'state': health.state,
                    'severity': health.severity,
                }
                status_code = 200
            except Exception as e:
                response_data = {
                    'uid': uid,
                    'message': str(e)
                }
                status_code = 400
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)

    def delete(self, request, uid=None, group=None, test=None):
        """Delete health by uid."""
        if uid and not test:
            try:
                self.health_model.objects.get(uid=uid).delete()
                response_data = {
                    'message': '{} deleted'.format(uid)
                }
                status_code = 200
            except Exception as e:
                response_data = {
                    'message': str(e)
                }
                status_code = 400
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)


class HealthTestView(View):
    def get(self, request, uid=None, test=None):
        """Get historical test results by uid and group."""
        pass

    def post(self, request, uid=None, test=None):
        """Post health test by uid and test."""
        kwargs = {}
        response_data = {}

        if request.POST:
            for key, value in request.POST.items():
                kwargs[key] = value

        # calculate health score: red, orange, yellow, green
        try:
            model = HealthTest._get_model(test)
            result = model.create(uid=uid, **kwargs)
        except Exception as e:
            response_data['message'] = str(e)
            status_code = 400
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)

        score = result.score(**kwargs)
        response_data['score'] = score
        response_data['message'] = '{} score changed to {} for uid {}'.format(test, score, uid)

        return HttpResponse(json.dumps(response_data), content_type="application/json")
