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
from django.db import models

from health_monitor.models import Health, HealthAlarm, HealthTest


class BodyHealth(Health):
    pass


class BodyHealthAlarm(HealthAlarm):
    health_model = BodyHealth


class HeartHealthTest(HealthTest):
    heartrate = models.IntegerField()

    health_model = BodyHealth
    groups = ['doctor']
    test = 'heart'

    @staticmethod
    def score(heartrate, **kwargs):
        heartrate = int(heartrate)
        if heartrate > 120:
            return 4
        elif heartrate > 100:
            return 3
        elif heartrate > 80:
            return 2
        else:
            return 1


class SleepHealthTest(HealthTest):
    hours = models.FloatField()

    health_model = BodyHealth
    groups = ['doctor', 'coach']
    test = 'sleep'

    @staticmethod
    def score(hours, **kwargs):
        hours = float(hours)
        if hours < 4:
            return 4
        elif hours < 6:
            return 3
        elif hours < 8:
            return 2
        else:
            return 1


class SmokeHealthTest(HealthTest):
    smokes = models.BooleanField(default=0)

    health_model = BodyHealth
    groups = ['doctor']
    test = 'smoke'

    @staticmethod
    def score(smokes, **kwargs):
        smokes = bool(smokes)
        if smokes:
            return 3
        else:
            return 1
