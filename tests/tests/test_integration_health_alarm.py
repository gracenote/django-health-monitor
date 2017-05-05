import json

from django.test import TestCase

from ..models import BodyHealthAlarm, BodyHealth, HeartHealthTest


class HealthAlarmModelIntegrationTestCase(TestCase):
    def test_health_test_history_caching(self):
        """Set up the following test results and get health-test history from health history.

           t1   t2   t3
        2: 65,  94,  115

          t1 t2 t3
        2: 1, 2, 3
        """

        HeartHealthTest.create(uid=2, heartrate=65)
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [1])
        HeartHealthTest.create(uid=2, heartrate=94)
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [2])
        HeartHealthTest.create(uid=2, heartrate=115)
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [3])

        self.assertEqual(BodyHealth.objects.get(uid=2).get_history(test='heart', repetition=2), [3, 2])
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [3, 2])
        self.assertEqual(BodyHealth.objects.get(uid=2).get_history(test='heart', repetition=3), [3, 2, 1])
        self.assertEqual(BodyHealth.objects.get(uid=2).history['heart'], [3, 2, 1])

    def test_health_alarm(self):
        """Set up the following test results and resulting health scores.

        Check that health state histories are created in the process after alarms are queried.

           t1   t2   t3   t4   t5
        1: 61,  63,  81,  69,  62
        2: 65,  94,  115, 112, 110
        3: 119, 110, 111,  94, 59

          t1 t2 t3 t4 t5
        1: 1, 1, 2, 1, 1
        2: 1, 2, 3, 3, 3
        3: 3, 3, 3, 2, 1
        """

        # @t1
        HeartHealthTest.create(uid=1, heartrate=61)
        HeartHealthTest.create(uid=2, heartrate=65)
        HeartHealthTest.create(uid=3, heartrate=119)

        # check alarm status
        result = BodyHealthAlarm.calculate_alarms(group='doctor', test='heart', score=2)
        self.assertEqual({3}, set(result))

        # check history
        self.assertEqual([1], BodyHealth.objects.get(uid=1).history['heart'])
        self.assertEqual([1], BodyHealth.objects.get(uid=2).history['heart'])
        self.assertEqual([3], BodyHealth.objects.get(uid=3).history['heart'])

        # @t2
        HeartHealthTest.create(uid=1, heartrate=63)
        HeartHealthTest.create(uid=2, heartrate=94)
        HeartHealthTest.create(uid=3, heartrate=110)

        # check history
        self.assertEqual([1], BodyHealth.objects.get(uid=1).history['heart'])
        self.assertEqual([2], BodyHealth.objects.get(uid=2).history['heart'])
        self.assertEqual([3], BodyHealth.objects.get(uid=3).history['heart'])

        # @t3
        HeartHealthTest.create(uid=1, heartrate=81)
        HeartHealthTest.create(uid=2, heartrate=115)
        HeartHealthTest.create(uid=3, heartrate=111)

        # check alarm status
        result = BodyHealthAlarm.calculate_alarms(group='doctor', test='heart', score=2, repetition=2)
        self.assertEqual({2, 3}, set(result))

        # check history
        self.assertEqual([2, 1], BodyHealth.objects.get(uid=1).history['heart'])
        self.assertEqual([3, 2], BodyHealth.objects.get(uid=2).history['heart'])
        self.assertEqual([3, 3], BodyHealth.objects.get(uid=3).history['heart'])

        # @t4
        HeartHealthTest.create(uid=1, heartrate=69)
        HeartHealthTest.create(uid=2, heartrate=112)
        HeartHealthTest.create(uid=3, heartrate=94)

        # check history
        self.assertEqual([1, 2], BodyHealth.objects.get(uid=1).history['heart'])
        self.assertEqual([3, 3], BodyHealth.objects.get(uid=2).history['heart'])
        self.assertEqual([2, 3], BodyHealth.objects.get(uid=3).history['heart'])

        # @t5
        HeartHealthTest.create(uid=1, heartrate=62)
        HeartHealthTest.create(uid=2, heartrate=110)
        HeartHealthTest.create(uid=3, heartrate=59)

        # check alarm status
        result = BodyHealthAlarm.calculate_alarms(group='doctor', test='heart', score=2, repetition=3, repetition_percent=25)
        self.assertEqual({1, 2, 3}, set(result))
        result = BodyHealthAlarm.calculate_alarms(group='doctor', test='heart', score=2, repetition=3)
        self.assertEqual({2}, set(result))

        # check history
        self.assertEqual([1, 1, 2], BodyHealth.objects.get(uid=1).history['heart'])
        self.assertEqual([3, 3, 3], BodyHealth.objects.get(uid=2).history['heart'])
        self.assertEqual([1, 2, 3], BodyHealth.objects.get(uid=3).history['heart'])


class HealthAlarmAPIIntegrationTestCase(TestCase):
    def setUp(self):
        """Set up the following test results and resulting health scores

           t1   t2   t3   t4   t5
        1: 61,  63,  81,  69,  62
        2: 65,  94,  115, 112, 110
        3: 119, 110, 111,  94, 59

          t1 t2 t3 t4 t5
        1: 1, 1, 2, 1, 1
        2: 1, 2, 3, 3, 3
        3: 3, 3, 3, 2, 1
        """
        # t1
        self.client.post('/health_test/heart/1/', {'heartrate': 61})
        self.client.post('/health_test/heart/2/', {'heartrate': 65})
        self.client.post('/health_test/heart/3/', {'heartrate': 119})
        # t2
        self.client.post('/health_test/heart/1/', {'heartrate': 63})
        self.client.post('/health_test/heart/2/', {'heartrate': 94})
        self.client.post('/health_test/heart/3/', {'heartrate': 110})
        # t3
        self.client.post('/health_test/heart/1/', {'heartrate': 81})
        self.client.post('/health_test/heart/2/', {'heartrate': 115})
        self.client.post('/health_test/heart/3/', {'heartrate': 111})
        # t4
        self.client.post('/health_test/heart/1/', {'heartrate': 69})
        self.client.post('/health_test/heart/2/', {'heartrate': 112})
        self.client.post('/health_test/heart/3/', {'heartrate': 94})
        # t5
        self.client.post('/health_test/heart/1/', {'heartrate': 62})
        self.client.post('/health_test/heart/2/', {'heartrate': 110})
        self.client.post('/health_test/heart/3/', {'heartrate': 59})

    def test_get_health_alarm_groups(self):
        response = self.client.get('/health_alarm/')
        content = json.loads(response.content.decode())
        self.assertEqual({"message": "group required"}, content)

    def test_get_health_alarm_group_tests(self):
        response = self.client.get('/health_alarm/doctor/')
        content = json.loads(response.content.decode())
        self.assertTrue('heart' in content['tests'])
        self.assertTrue('sleep' in content['tests'])

    def test_get_health_alarm_test(self):
        response = self.client.get('/health_alarm/doctor/heart/?score=3')
        content = json.loads(response.content.decode())
        self.assertEqual({2}, set(content))

        response = self.client.get('/health_alarm/doctor/heart/?score=2&repetition=3&repetition_percent=25')
        content = json.loads(response.content.decode())
        self.assertEqual({1, 2, 3}, set(content))

        response = self.client.get('/health_alarm/doctor/heart/?score=2&repetition=3')
        content = json.loads(response.content.decode())
        self.assertEqual({2}, set(content))
