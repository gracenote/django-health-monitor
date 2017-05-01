from django.test import TestCase
from django.utils import timezone

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

    def test_datetime(self):
        now = timezone.now()
        SleepHealthTest.create(uid=1, hours=8)
        result = SleepHealthTest.objects.last()

        self.assertGreater(result.time, now)

    def test_get_history(self):
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=3, hours=8)
        SleepHealthTest.create(uid=3, hours=8)
        time_1 = timezone.now()
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=3, hours=8)
        time_2 = timezone.now()
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=3, hours=8)

        results = SleepHealthTest.get_history(uids=[1, 2, 3])
        self.assertEqual(12, len(results))
        results = SleepHealthTest.get_history(uids=[1])
        self.assertEqual(4, len(results))
        results = SleepHealthTest.get_history(uids=[1, 2, 3], end_time=time_1)
        self.assertEqual(6, len(results))
        results = SleepHealthTest.get_history(uids=[1, 2, 3], start_time=time_1, end_time=time_2)
        self.assertEqual(3, len(results))
        results = SleepHealthTest.get_history(uids=[1, 2, 3], start_time=time_2)
        self.assertEqual(3, len(results))
        results = SleepHealthTest.get_history(uids=[2], start_time=time_1)
        self.assertEqual(2, len(results))
        results = SleepHealthTest.get_history(uids=[2], start_time=time_2)
        self.assertEqual(1, len(results))

    def test_get_score(self):
        s = SleepHealthTest.create(uid=1, hours=8)
        self.assertEqual(1, s.get_score())

        s.hours = 5.5
        s.save()
        self.assertEqual(3, s.get_score())
