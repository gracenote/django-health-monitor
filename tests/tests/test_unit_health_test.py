from django.test import TestCase

from ..models import BodyHealth, HeartHealthTest, SleepHealthTest


class HealthTestUnitTestCase(TestCase):
    def test_heart(self):
        HeartHealthTest.create(uid=1, heartrate=60)
        HeartHealthTest.create(uid=1, heartrate=60)
        self.assertEqual(2, len(HeartHealthTest.objects.all()))
        body_health = BodyHealth.objects.get(uid=1)
        self.assertEqual(1, body_health.state['doctor']['heart']['score'])

    def test_sleep(self):
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=1, hours=8)
        self.assertEqual(2, len(SleepHealthTest.objects.all()))
        body_health = BodyHealth.objects.get(uid=1)
        self.assertEqual(1, body_health.state['doctor']['sleep']['score'])
