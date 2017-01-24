from django.test import TestCase
from health_monitor.models import Health


class HealthUnitTestCase(TestCase):

    def test_update_score(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]
        health.update_score(test_name='volume', score=2)

        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['audio']['volume']['score'], 2)
        self.assertEqual(health.severity['audio'], 2)
