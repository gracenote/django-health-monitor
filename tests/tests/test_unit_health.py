import time

from django.test import TestCase

from ..models import BodyHealth


class HealthUnitTestCase(TestCase):
    def test_update_score(self):
        uid = 123456789
        health = BodyHealth.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test='heart', score=2)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 2)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # set sleep score to 3, check severity is 3
        health.update_score(test='sleep', score=3)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 3)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # set heart score to 1, check severity is 3 since sleep score is still 3
        health.update_score(test='heart', score=1)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 1)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # set sleep score to 1, check severity is 1
        health.update_score(test='sleep', score=1)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 1)
        self.assertEqual(health.severity['doctor']['score'], 1)

    def test_delete_test(self):
        uid = 123456789
        health = BodyHealth.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test='heart', score=2)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 2)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # set sleep score to 3, check severity is 3
        health.update_score(test='sleep', score=3)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 3)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # delete sleep test
        health.delete_test(test='sleep')
        self.assertTrue('sleep' not in health.state['doctor'].keys())
        self.assertEqual(health.severity['doctor']['score'], 2)

        # delete heart test
        health.delete_test(test='heart')
        self.assertTrue('heart' not in health.state['doctor'].keys())
        self.assertEqual(health.severity['doctor']['score'], 1)

    def test_updated_at(self):
        uid = 123456789
        health = BodyHealth.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test='heart', score=2)
        health = BodyHealth.objects.get(uid=uid)
        self.assertTrue(health.state['doctor']['heart']['updated'])
        self.assertTrue(health.severity['doctor']['updated'])

    def test_change_update_date_on_score_change(self):
        uid = 123456789
        health = BodyHealth.objects.get_or_create(uid=uid)[0]

        # set heart score to 2
        health.update_score(test='heart', score=2)
        health = BodyHealth.objects.get(uid=uid)

        # set heart score to 3, check 'update' does change
        old_state_time = health.state['doctor']['heart']['updated']
        old_severity_time = health.severity['doctor']['updated']
        time.sleep(0.001)
        health.update_score(test='heart', score=3)
        health = BodyHealth.objects.get(uid=uid)
        self.assertNotEqual(old_state_time, health.state['doctor']['heart']['updated'])
        self.assertNotEqual(old_severity_time, health.severity['doctor']['updated'])

        # set heart score to 3, check 'update' does not change
        old_state_time = health.state['doctor']['heart']['updated']
        old_severity_time = health.severity['doctor']['updated']
        time.sleep(0.001)
        health.update_score(test='heart', score=3)
        health = BodyHealth.objects.get(uid=uid)
        self.assertEqual(old_state_time, health.state['doctor']['heart']['updated'])
        self.assertEqual(old_severity_time, health.severity['doctor']['updated'])
