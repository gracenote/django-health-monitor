from django.db import models

from health_monitor.models import Health, HealthTest


class BodyHealth(Health):
    pass


class HeartHealthTest(HealthTest):
    heartrate = models.IntegerField()

    health_model = BodyHealth
    groups = ['doctor']
    test = 'heart'

    @staticmethod
    def score(heartrate):
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
    def score(hours):
        hours = float(hours)
        if hours < 4:
            return 4
        elif hours < 6:
            return 3
        elif hours < 8:
            return 2
        else:
            return 1
