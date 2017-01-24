import json

from django.test import TestCase
from health_monitor.models import Health


class HealthIntegrationTestCase(TestCase):
    def test_volume_for_subscriber_audio(self):
        uid = 123456789
        # change volume state to 2 and check severity
        response = self.client.get('/health/123456789/update/volume/?volume=-60')
        self.assertContains(response, 'changed to 2')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['audio'], 2)
        # change volume state back to 1 and check severity
        response = self.client.get('/health/123456789/update/volume/?volume=-1')
        self.assertContains(response, 'changed to 1')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['audio'], 1)

        # change volume and datarate and check higher severity
        response = self.client.get('/health/123456789/update/volume/?volume=0')
        self.assertContains(response, 'changed to 4')
        response = self.client.get('/health/123456789/update/datarate/?datarate=60')
        self.assertContains(response, 'changed to 3')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['audio'], 4)

        # change volume using alias and check for higher severity
        response = self.client.get('/health/123456789/update/volume/?volume=-60')
        self.assertContains(response, 'changed to 2')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.severity['audio'], 3)

    def test_mp3_submit(self):
        uid = 123456789
        response = self.client.get('/health/123456789/update/mp3_submit/?mp3_present=0')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['audio']['mp3_submit']['score'], 2)
        self.assertContains(response, 'changed to 2')
        response = self.client.get('/health/123456789/update/mp3_submit/?mp3_present=1')
        health = Health.objects.get(uid=uid)
        self.assertEqual(health.state['audio']['mp3_submit']['score'], 1)
        self.assertContains(response, 'changed to 1')

    def test_mp3_match(self):
        uid = 123456789
        response = self.client.get('/health/123456789/update/mp3_match/?match_status=0')
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['audio']['mp3_match']['score'], 3)
        response = self.client.get('/health/123456789/update/mp3_match/?match_status=1')
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['audio']['mp3_match']['score'], 1)

    # def test_bis_queue(self):
    #     uid = 123456789
    #     uid2 = 987654321
    #
    #     response = self.client.get('/health/bulk_update/bis/11111111/bis_queue/?submit_queue_lv=0&submit_queue_sac=0&submit_queue_sc=0')
    #     failures = [x['status'] for x in json.loads(response.content.decode())['responses'] if x['status'] != 'success']
    #     self.assertEqual(len(failures), 0)
    #     health = Health.objects.get(uid=uid)
    #     self.assertEqual(health.state['audio']['bis_queue']['score'], 1)
    #     health = Health.objects.get(uid=uid2)
    #     self.assertEqual(health.state['audio']['bis_queue']['score'], 1)
    #
    #     response = self.client.get('/health/bulk_update/bis/11111111/bis_queue/?submit_queue_lv=501&submit_queue_sac=0&submit_queue_sc=101')
    #     health = Health.objects.get(uid=uid)
    #     failures = [x['status'] for x in json.loads(response.content.decode())['responses'] if x['status'] != 'success']
    #     self.assertEqual(len(failures), 0)
    #     self.assertEqual(health.state['audio']['bis_queue']['score'], 3)
    #     health = Health.objects.get(uid=uid2)
    #     self.assertEqual(health.state['audio']['bis_queue']['score'], 3)

    # def test_bis_connection(self):
    #     uid = 123456789
    #     uid2 = 987654321
    #
    #     response = self.client.get('/health/bulk_update/bis/11111111/bis_connection/?bis_status_lv=OK&bis_status_sac=OK&bis_status_sc=OK')
    #     failures = [x['status'] for x in json.loads(response.content.decode())['responses'] if x['status'] != 'success']
    #     self.assertEqual(len(failures), 0)
    #     health = Health.objects.get(uid=uid)
    #     self.assertEqual(health.state['audio']['bis_connection']['score'], 1)
    #     health = Health.objects.get(uid=uid2)
    #     self.assertEqual(health.state['audio']['bis_connection']['score'], 1)
    #
    #     response = self.client.get('/health/bulk_update/bis/11111111/bis_connection/?bis_status_lv=BAD&bis_status_sac=BAD&bis_status_sc=BAD')
    #     failures = [x['status'] for x in json.loads(response.content.decode())['responses'] if x['status'] != 'success']
    #     self.assertEqual(len(failures), 0)
    #     health = Health.objects.get(uid=uid)
    #     self.assertEqual(health.state['audio']['bis_connection']['score'], 4)
    #     health = Health.objects.get(uid=uid2)
    #     self.assertEqual(health.state['audio']['bis_connection']['score'], 4)

    def test_epg_overlap(self):
        uid = 123456789
        response = self.client.get('/health/123456789/update/epg_overlap/?overlap_count=0')
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to None')
        self.assertEqual(health.state['audio']['epg_overlap']['score'], None)
        response = self.client.get('/health/123456789/update/epg_overlap/?overlap_count=1')
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 2')
        self.assertEqual(health.state['audio']['epg_overlap']['score'], 2)

    def test_epg_gap(self):
        uid = 123456789
        response = self.client.get('/health/123456789/update/epg_gap/?gap_count=0')
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to None')
        self.assertEqual(health.state['audio']['epg_gap']['score'], None)
        response = self.client.get('/health/123456789/update/epg_gap/?gap_count=1')
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 2')
        self.assertEqual(health.state['audio']['epg_gap']['score'], 2)

    # def test_subscribed(self):
    #     uid = 123456789
    #     uid2 = 987654321
    #     response = self.client.get('/health/{}/update/subscribed/?tui={}&live_tier=1&shift_tier=1'.format(uid, uid))
    #     health = Health.objects.get(uid=uid)
    #     self.assertContains(response, 'changed to 1')
    #     self.assertEqual(health.state['audio']['subscribed']['score'], 1)
    #     # Under subscribed shift
    #     self.client.get('/health/{}/update/subscribed/?tui={}&live_tier=1&shift_tier=0'.format(uid, uid))
    #     health = Health.objects.get(uid=uid)
    #     self.assertEqual(health.state['audio']['subscribed']['score'], 4)
    #     # Under subscribed live
    #     self.client.get('/health/{}/update/subscribed/?tui={}&live_tier=0&shift_tier=1'.format(uid, uid))
    #     health = Health.objects.get(uid=uid)
    #     self.assertEqual(health.state['audio']['subscribed']['score'], 4)
    #     # Over subscribed
    #     self.client.get('/health/{}/update/subscribed/?tui={}&live_tier=1&shift_tier=1'.format(uid2, uid2))
    #     health = Health.objects.get(uid=uid2)
    #     self.assertEqual(health.state['audio']['subscribed']['score'], 2)
    #     # test yes no values
    #     self.client.get('/health/{}/update/subscribed/?tui={}&live_tier=Yes&shift_tier=No'.format(uid, uid))
    #     health = Health.objects.get(uid=uid)
    #     self.assertEqual(health.state['audio']['subscribed']['score'], 4)

    def test_eam_api_match(self):
        uid = 123456789
        # eam_api_match: True
        response = self.client.get('/health/{}/update/eam_api_match/?api_match=1&ens_status=active'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['eam_api_match']['score'], 1)
        # eam_api_match: False
        response = self.client.get('/health/{}/update/eam_api_match/?api_match=0&ens_status=active'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['video']['eam_api_match']['score'], 4)

    def test_eam_api_status(self):
        uid = 123456789
        # eam_api_status: ens_status = 'active', use = True, status = 'ON' (green)
        response = self.client.get('/health/{}/update/eam_api_status/?ens_status=active&use=1&status=ON'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['eam_api_status']['score'], 1)
        # eam_api_status: ens_status = 'active', use = True, status = 'OFF' (orange)
        response = self.client.get('/health/{}/update/eam_api_status/?ens_status=active&use=1&status=OFF'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['eam_api_status']['score'], 3)
        # eam_api_status: ens_status = 'active', use = False, status = 'OFF' (orange)
        response = self.client.get('/health/{}/update/eam_api_status/?ens_status=active&use=0&status=OFF'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['video']['eam_api_status']['score'], 4)
        # eam_api_status: ens_status = 'inactive', use = False, status = 'OFF' (green)
        response = self.client.get('/health/{}/update/eam_api_status/?ens_status=inactive&use=0&status=OFF'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['eam_api_status']['score'], 1)
        # eam_api_status: ens_status = 'inactive', use = True, status = 'OFF' (green)
        response = self.client.get('/health/{}/update/eam_api_status/?ens_status=inactive&use=1&status=OFF'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['eam_api_status']['score'], 1)
        # eam_api_status: ens_status = 'inactive', use = True, status = 'ON' (orange)
        response = self.client.get('/health/{}/update/eam_api_status/?ens_status=inactive&use=1&status=ON'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['eam_api_status']['score'], 3)

    def test_ec_status_audio(self):
        uid = 123456789
        # ec_status_audio: audio = 'DECODING' (green)
        response = self.client.get('/health/{}/update/ec_status_audio/?audio=DECODING'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['audio']['ec_status_audio']['score'], 1)
        self.assertEqual(health.state['video']['ec_status_audio']['score'], 1)
        # ec_status_audio: audio = 'NOT READY YET' (red)
        response = self.client.get('/health/{}/update/ec_status_audio/?audio=NOT%20READY%20YET'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['audio']['ec_status_audio']['score'], 4)
        self.assertEqual(health.state['video']['ec_status_audio']['score'], 4)
        # ec_status_audio: audio = 'DECODING', video = 'STOPPED' (orange)
        response = self.client.get('/health/{}/update/ec_status_audio/?audio=STOPPED'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['audio']['ec_status_audio']['score'], 3)
        self.assertEqual(health.state['video']['ec_status_audio']['score'], 3)

    def test_ec_status_video(self):
        uid = 123456789
        # ec_status_video: video = 'DECODING' (green)
        response = self.client.get('/health/{}/update/ec_status_video/?video=DECODING'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['ec_status_video']['score'], 1)
        # ec_status_video: video = 'NOT READY YET' (red)
        response = self.client.get('/health/{}/update/ec_status_video/?video=NOT%20READY%20YET'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['video']['ec_status_video']['score'], 4)
        # ec_status_video: video = 'STOPPED' (orange)
        response = self.client.get('/health/{}/update/ec_status_video/?video=STOPPED'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['ec_status_video']['score'], 3)

    def test_ec_status_network(self):
        uid = 123456789
        # ec_status_network: network = 'BAD' (red)
        response = self.client.get('/health/{}/update/ec_status_network/?network=BAD'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['video']['ec_status_network']['score'], 4)
        # ec_status_network: network = 'GOOD' (green)
        response = self.client.get('/health/{}/update/ec_status_network/?network=GOOD'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['ec_status_network']['score'], 1)

    def test_ec_status_qsize(self):
        uid = 123456789
        # ec_status_qsize: qsize = 8000 (orange)
        response = self.client.get('/health/{}/update/ec_status_qsize/?qsize=8000'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['ec_status_qsize']['score'], 3)
        # ec_status_qsize: qsize = 10 (green)
        response = self.client.get('/health/{}/update/ec_status_qsize/?qsize=10'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['ec_status_qsize']['score'], 1)

    def test_ec_status_v_fps(self):
        uid = 123456789
        # ec_status_v_fps: v_fps = 9 (green)
        response = self.client.get('/health/{}/update/ec_status_v_fps/?v_fps=9'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['ec_status_v_fps']['score'], 1)
        # ec_status_v_fps: v_fps = 5 (orange)
        response = self.client.get('/health/{}/update/ec_status_v_fps/?v_fps=5'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['ec_status_v_fps']['score'], 3)

    def test_ec_status_v_delay(self):
        uid = 123456789
        # ec_status_v_delay: v_delay = 5 (green)
        response = self.client.get('/health/{}/update/ec_status_v_delay/?v_delay=5'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['ec_status_v_delay']['score'], 1)
        # ec_status_v_delay: v_delay = 9999 (green)
        response = self.client.get('/health/{}/update/ec_status_v_delay/?v_delay=9999'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['ec_status_v_delay']['score'], 3)

    def test_feature_proxy_delay(self):
        uid = 123456789
        # feature_proxy_delay: delay = 1 (green)
        response = self.client.get('/health/{}/update/feature_proxy_delay/?delay=1'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 1')
        self.assertEqual(health.state['video']['feature_proxy_delay']['score'], 1)
        # feature_proxy_delay: delay = 4 (yellow)
        response = self.client.get('/health/{}/update/feature_proxy_delay/?delay=4'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 3')
        self.assertEqual(health.state['video']['feature_proxy_delay']['score'], 3)
        # feature_proxy_delay: delay = 601 (red)
        response = self.client.get('/health/{}/update/feature_proxy_delay/?delay=601'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['video']['feature_proxy_delay']['score'], 4)
        # feature_proxy_delay: delay = None (red)
        response = self.client.get('/health/{}/update/feature_proxy_delay/?delay=None'.format(uid))
        health = Health.objects.get(uid=uid)
        self.assertContains(response, 'changed to 4')
        self.assertEqual(health.state['video']['feature_proxy_delay']['score'], 4)
