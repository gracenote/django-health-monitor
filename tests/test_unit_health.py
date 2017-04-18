import time

from django.test import TestCase

from health_monitor.models import Health, HealthTest


class HealthUnitTestCase(TestCase):
    def setUp(self):
        try:
            class Heart(HealthTest):
                test = 'heart'
                groups = ['doctor']

                def score(self, heartrate):
                    heartrate = int(heartrate)
                    if heartrate > 120:
                        return 4
                    elif heartrate > 100:
                        return 3
                    elif heartrate > 80:
                        return 2
                    else:
                        return 1

                class Meta(object):
                    app_label = 'health_monitor'

            class Sleep(HealthTest):

                test = 'sleep'
                groups = ['doctor']

                def score(self, hours):
                    hours = int(hours)
                    if hours < 4:
                        return 4
                    elif hours < 6:
                        return 3
                    elif hours < 8:
                        return 2
                    else:
                        return 1

                class Meta(object):
                    app_label = 'health_monitor'
        except Exception:
            pass

    def test_update_score(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test='heart', score=2)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 2)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # set sleep score to 3, check severity is 3
        health.update_score(test='sleep', score=3)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 3)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # set heart score to 1, check severity is 3 since sleep score is still 3
        health.update_score(test='heart', score=1)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 1)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # set sleep score to 1, check severity is 1
        health.update_score(test='sleep', score=1)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 1)
        self.assertEqual(health.severity['doctor']['score'], 1)

    def test_delete_test_state(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test='heart', score=2)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['heart']['score'], 2)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # set sleep score to 3, check severity is 3
        health.update_score(test='sleep', score=3)
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['doctor']['sleep']['score'], 3)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # delete sleep test
        health.delete_test_state(test='sleep')
        self.assertTrue('sleep' not in health.state['doctor'].keys())
        self.assertEqual(health.severity['doctor']['score'], 2)

        # delete heart test
        health.delete_test_state(test='heart')
        self.assertTrue('heart' not in health.state['doctor'].keys())
        self.assertEqual(health.severity['doctor']['score'], 1)

    def test_updated_at(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2, check severity is 2
        health.update_score(test='heart', score=2)
        health = Health.objects.get(uid=uid)
        self.assertTrue(health.state['doctor']['heart']['updated'])
        self.assertTrue(health.severity['doctor']['updated'])

    def test_change_update_date_on_score_change(self):
        uid = 123456789
        health = Health.objects.get_or_create(uid=uid)[0]

        # set heart score to 2
        health.update_score(test='heart', score=2)
        health = Health.objects.get(uid=uid)

        # set heart score to 3, check 'update' does change
        old_state_time = health.state['doctor']['heart']['updated']
        old_severity_time = health.severity['doctor']['updated']
        time.sleep(0.001)
        health.update_score(test='heart', score=3)
        health = Health.objects.get(uid=uid)
        self.assertNotEqual(old_state_time, health.state['doctor']['heart']['updated'])
        self.assertNotEqual(old_severity_time, health.severity['doctor']['updated'])

        # set heart score to 3, check 'update' does not change
        old_state_time = health.state['doctor']['heart']['updated']
        old_severity_time = health.severity['doctor']['updated']
        time.sleep(0.001)
        health.update_score(test='heart', score=3)
        health = Health.objects.get(uid=uid)
        self.assertEqual(old_state_time, health.state['doctor']['heart']['updated'])
        self.assertEqual(old_severity_time, health.severity['doctor']['updated'])
