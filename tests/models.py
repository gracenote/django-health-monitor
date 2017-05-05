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
