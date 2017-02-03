from django.test import TestCase
from health_monitor.models import Health


class HealthIntegrationTestCase(TestCase):
    def test_heart(self):
        uid = 123456789

        # change heart state and severity to 2
        response = self.client.get('/health/123456789/update/heart/?heartrate=100&arrhythmia=0', follow=True)
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 2')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['doctor'], 2)

        # change heart state and severity to 1
        response = self.client.get('/health/123456789/update/heart/?heartrate=60&arrhythmia=0', follow=True)
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 1')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['doctor'], 1)

        # change heart state and severity to 3
        response = self.client.get('/health/123456789/update/heart/?heartrate=60&arrhythmia=1', follow=True)
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 3')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['doctor'], 3)
