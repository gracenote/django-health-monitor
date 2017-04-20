import json

from django.test import TestCase

from ..models import BodyHealth


class HealthIntegrationTestCase(TestCase):
    def test_get_health(self):
        # check health does not exist
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/health_test/heart/123456789/', {'heartrate': 100})

        # check health does exist
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 200)

    def test_delete_health(self):
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

    def test_post_health_test(self):
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
