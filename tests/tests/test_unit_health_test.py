from django.test import TestCase

from ..models import BodyHealth, Heart, Sleep


class HealthTestUnitTestCase(TestCase):
    def test_heart(self):
        Heart.create(uid=1, heartrate=60)
        self.assertEqual(1, len(Heart.objects.all()))
        body_health = BodyHealth.objects.get(uid=1)
        self.assertEqual(1, body_health.state['doctor']['heart']['score'])

    def test_sleep(self):
        Sleep.create(uid=1, hours=8)
        self.assertEqual(1, len(Sleep.objects.all()))
        body_health = BodyHealth.objects.get(uid=1)
        self.assertEqual(1, body_health.state['doctor']['sleep']['score'])
