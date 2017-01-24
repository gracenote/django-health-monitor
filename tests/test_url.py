from django.test import TestCase
import json


class HealthUrlTestCase(TestCase):
    """Test correct urls for /health/<uid>/"""
    def test_get_uid(self):
        response = self.client.get('/health/123/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'failure')

        response = self.client.get('/health/123/update/volume/?volume=-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'success')

        response = self.client.get('/health/123/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'success')

    """Test incorrect urls for /health/<uid>/update/<test_name>/"""
    def test_update_missing_tui(self):
        response = self.client.get('/health//update/mp3_submit/?match_status=0&mp3_present=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'error')

    def test_update_wrong_test_name(self):
        response = self.client.get('/health/123/update/abc/?volume=-1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content.decode())['status'], 'error')

    def test_update_wrong_param(self):
        response = self.client.get('/health/123/update/datarate/?volume=-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode())['status'], 'error')

    """Test incorrect urls for /health/bulk_update/<model>/<uid>/<test_name>/"""
    # def test_bulk_update_missing_model(self):
    #     response = self.client.get('/health/bulk_update//11111111/datarate/?datarate=0')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content.decode())['status'], 'error')
    #
    # def test_bulk_update_missing_model_uid(self):
    #     response = self.client.get('/health/bulk_update/bis//datarate/?datarate=0')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content.decode())['status'], 'error')
    #
    # def test_bulk_update_missing_test_name(self):
    #     response = self.client.get('/health/bulk_update/bis/11111111//?datarate=0')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content.decode())['status'], 'error')

    """Test correct url for /health/snapshot/"""
    # def test_health_snapshot_audio(self):
    #     response = self.client.get('/health/snapshot/audio/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_health_snapshot_video(self):
    #     response = self.client.get('/health/snapshot/video/')
    #     self.assertEqual(response.status_code, 200)
