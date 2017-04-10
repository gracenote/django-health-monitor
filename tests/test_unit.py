from django.test import TestCase
from health_monitor.models import Health


class HealthUnitTestCase(TestCase):

    def test_update_score(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test_name='heart', score=2)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 2)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # set sleep score to 3, check severity is 3
        health.update_score(test_name='sleep', score=3)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 3)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # set heart score to 1, check severity is 3 since sleep score is still 3
        health.update_score(test_name='heart', score=1)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 1)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # set sleep score to 1, check severity is 1
        health.update_score(test_name='sleep', score=1)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 1)
        self.assertEqual(health.severity['doctor']['score'], 1)

    def test_delete_test_state(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test_name='heart', score=2)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 2)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # set sleep score to 3, check severity is 3
        health.update_score(test_name='sleep', score=3)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 3)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # delete sleep test
        health.delete_test_state(test_name='sleep')
        self.assertTrue('sleep' not in health.state['doctor'].keys())
        self.assertEqual(health.severity['doctor']['score'], 2)

        # delete heart test
        health.delete_test_state(test_name='heart')
        self.assertTrue('heart' not in health.state['doctor'].keys())
        self.assertEqual(health.severity['doctor']['score'], 1)

    def test_updated_at(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test_name='heart', score=2)
        health = Health.objects.get(uid=uid)
        self.assertTrue(health.state['doctor']['heart']['updated'])
        self.assertTrue(health.severity['doctor']['updated'])
