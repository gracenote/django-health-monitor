import json

from django.test import TestCase
from django.utils import timezone

from ..models import BodyHealth, SleepHealthTest
from health_monitor import utils


class HealthIntegrationTestCase(TestCase):
    def test_get_health(self):
        # check health does not exist
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/health_test/heart/123456789/', {'heartrate': 100})

        # check health does exist
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 200)

    def test_delete_health_uid(self):
        """DELETE the health for a particular uid - /health/<uid>/"""
        # post test result to 123456789
        response = self.client.post('/health_test/heart/123456789/', {'heartrate': 100})
        self.assertEqual(response.status_code, 200)

        # check 123456789 is in list of uids
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(123456789 in json.loads(response.content.decode())['uids'])

        # delete 123456789
        response = self.client.delete('/health/123456789/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/health/')
        self.assertTrue(123456789 not in json.loads(response.content.decode())['uids'])

        # delete nonexistent asset
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 400)

    def test_get_health_test(self):
        """GET a list of all health tests - /health_test/"""
        response = self.client.get('/health_test/')
        self.assertTrue('sleep' in json.loads(response.content.decode())['tests'])
        self.assertTrue('heart' in json.loads(response.content.decode())['tests'])

    def test_get_health_test_history(self):
        """GET test results for a particular test with filters - /health_tests/<test>/?uids=<uids>&start_time=<start_time>&end_time=<end_time>

        GET test results for a particular test and uid with filters - /health_test/<test>/<uid>/?start_time=<start_time>&end_time=<end_time>
        """
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=3, hours=8)
        SleepHealthTest.create(uid=3, hours=8)
        time_1 = utils.datetime_to_iso(timezone.now())
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=3, hours=8)
        time_2, _ = utils.datetime_to_iso(timezone.now()).split('+')  # missing UTC offset - will generate naive datetime warning
        SleepHealthTest.create(uid=1, hours=8)
        SleepHealthTest.create(uid=2, hours=8)
        SleepHealthTest.create(uid=3, hours=8)

        response = self.client.get('/health_test/sleep/?uids=1,2,3')
        content = json.loads(response.content)
        self.assertEqual(12, len(content))
        response = self.client.get('/health_test/sleep/1/')
        content = json.loads(response.content)
        self.assertEqual(4, len(content))
        response = self.client.get('/health_test/sleep/?uids=1,2,3&end_time={}'.format(time_1))
        content = json.loads(response.content)
        self.assertEqual(6, len(content))
        response = self.client.get('/health_test/sleep/?uids=1,2,3&start_time={}&end_time={}'.format(time_1, time_2))
        content = json.loads(response.content)
        self.assertEqual(3, len(content))
        response = self.client.get('/health_test/sleep/?uids=1,2,3&start_time={}'.format(time_2))
        content = json.loads(response.content)
        self.assertEqual(3, len(content))
        response = self.client.get('/health_test/sleep/2/?start_time={}'.format(time_1))
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        response = self.client.get('/health_test/sleep/2/?start_time={}'.format(time_2))
        content = json.loads(response.content)
        self.assertEqual(1, len(content))

    def test_post_health_test(self):
        """POST test results for a particular test and uid - /health_test/<test>/<uid>/"""
        # change heart state and severity to 2
        response = self.client.post('/health_test/heart/123456789/', {'heartrate': 100})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'changed to 2')
        health = BodyHealth.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # change sleep state and severity to 3
        response = self.client.post('/health_test/sleep/123456789/', {'hours': 4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'changed to 3')
        health = BodyHealth.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # change heart state and severity to 1
        response = self.client.post('/health_test/heart/123456789/', {'heartrate': 60})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'changed to 1')
        health = BodyHealth.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # change sleep state and severity to 3
        response = self.client.post('/health_test/sleep/123456789/', {'hours': 8})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'changed to 1')
        health = BodyHealth.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 1)

        # check overall status
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 200)

    def test_post_health_test_wrong_test_name(self):
        response = self.client.post('/health_test/breath/123456789/', {'heartrate': 60})
        self.assertEqual(response.status_code, 400)

    def test_post_health_test_wrong_param(self):
        response = self.client.post('/health_test/heart/123456789/', {'breath': 1})
        self.assertEqual(response.status_code, 400)
