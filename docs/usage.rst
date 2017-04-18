#####
Usage
#####

To use Django Health Monitor in an application, there are three main steps:

1. Define Models
2. Configure API
3. Customize Notification Filters (optional)


****************
1. Define Models
****************

Two main types of models are needed to track a system's state and to capture test results - `Health` and `HealthTest`.

The base `Health` model serves the purpose of storing an asset's latest "health test" results from a variety tests, normalized as test "scores" in a "health state". Additionally, the highest result from the normalized test scores equals an asset's "health severity", which is used to quickly highlight which assets have an elevated status and should be investigated.

To explain this concept, let's say that an overall `BodyHealth` depends on a "heart" test result and a "sleep" test result, each of which have four normalized test scores - 1 for good, 2 for mildly bad, 3 for moderately bad, and 4 for extremely bad. For a particular person, a "heart" score of 3 and a "sleep" score of 2 would result in a state of `{'heart': 3, 'sleep': 2}` and a severity of 3. If later the "sleep" score changed to 1, the state will change to `{'heart': 3, 'sleep': 1}` and remain a severity of 3 since severity is calculated as the max score within state. If later the "heart" score changed to 1, the resultant state would be `{'heart': 1, 'sleep': 1}` and the severity would drop to 1 indicating an overall "good" health.

Defining a child class of `Health` is as simple as the following where `uid` is set as a model attribute with a unique constraint. An `IntField` is recommended.

    models.py::

        from health_monitor.models import Health


        class BodyHealth(Health):
            uid = models.IntField(primary_key=True, db_index=True)


The base `HealthTest` model serves the purpose of storing historical test results, turning raw test results into normalized scores, and automatically updating the overall health. For this example, let us define two health tests - `HeartHealthTest` and `SleepHealthTest`.

    models.py::

        from health_monitor.models import HealthTest


        class HeartHealthTest(HealthTest):
            uid = models.IntField(db_index=True)
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

        class SleepHealthTest(HealthTest):
            uid = models.IntField(db_index=True)
            test = 'sleep'
            groups = ['doctor']

            def score(self, hours):
                if sleep < 4:
                    return 4
                elif sleep < 6:
                    return 3
                elif sleep < 8:
                    return 2
                else:
                    return 1

In these examples of `HealthHealthTest` and `SleepHealthTest`, there are two attributes that are also required - `test` and `groups`. `test` is a string that will be used to reference the test in the API (following section) and `groups` is a list of groups that each test will be associated with. Each test must belong to at least one group, and each group serves the purposes of bunching related tests. Note that the `uid` should be set to be the same type as above in `BodyHealth`, however, it should **not** be set as a primary key.


****************
2. Configure API
****************

The following steps create an API with the following endpoints and actions:

- /health/
    - GET a list of all health uids
- /health/<uid>/
    - GET the health states and health severities of a particular uid
    - DELETE the health instance for a particular uid
- /health/<uid>/<test>/
    - POST test results for a particular uid

Where:

- <uid> is a unique identifier for the asset.
- <test> is the name of a health test.

Map URLs to Views
-----------------
    urls.py::


        from django.conf.urls import url

        from health_monitor import views


        urlpatterns = [
            url(r'^health/$', views.HealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/$', views.HealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/(?P<test>[\w]*)/$', views.HealthView.as_view()),
            # url(r'^health/(?P<uid>[\d]*)/history/(?P<group>[\w-]*)/$', views.history, name='history'),
        ]


*********************************
3. Customize Notification Filters
*********************************
TODO
