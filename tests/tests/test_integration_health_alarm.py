from django.test import TestCase

from ..models import BodyHealth, HeartHealthTest


class HealthAlarmModelIntegrationTestCase(TestCase):
    def test_health_test_history_caching(self):
        """Set up the following test results and get health-test history from health history.

           t1   t2   t3
        2: 65,  94,  115

          t1 t2 t3
        2: 1, 2, 3
        """

        HeartHealthTest.create(uid=2, heartrate=65)
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [1])
        HeartHealthTest.create(uid=2, heartrate=94)
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [2])
        HeartHealthTest.create(uid=2, heartrate=115)
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [3])

        self.assertEqual(BodyHealth.objects.get(uid=2).get_history(test='heart', repetition=2), [3, 2])
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [3, 2])
        self.assertEqual(BodyHealth.objects.get(uid=2).get_history(test='heart', repetition=3), [3, 2, 1])
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [3, 2, 1])
