from django.test import TestCase
import json


class HealthUrlTestCase(TestCase):
    """Test correct urls for /health/<uid>/"""
    def test_get_uid(self):
        response = self.client.get('/health/123/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'failure')

        response = self.client.get('/health/123/update/heart/?heartrate=60&arrhythmia=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'success')

        response = self.client.get('/health/123/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'success')

    """Test incorrect urls for /health/<uid>/update/<test_name>/"""
    def test_update_wrong_test_name(self):
        response = self.client.get('/health/123/update/abc/?heartrate=60&arrhythmia=0')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content.decode())['status'], 'error')

    def test_update_wrong_param(self):
        response = self.client.get('/health/123/update/heart/?breath=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'error')
