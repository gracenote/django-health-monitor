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

`Health`
--------

The base `Health` model serves the purpose of storing an asset's latest "health test" results from a variety tests, normalized as test "scores" in a "health state". Additionally, the highest result from the normalized test scores equals an asset's "health severity", which is used to quickly highlight which assets have an elevated status and should be investigated.

To explain this concept, let's say that an overall `BodyHealth` depends on a "heart" test result and a "sleep" test result, each of which have four normalized test scores - 1 for good, 2 for mildly bad, 3 for moderately bad, and 4 for extremely bad. For a particular person, a "heart" score of 3 and a "sleep" score of 2 would result in a state of `{'heart': 3, 'sleep': 2}` and a severity of 3. If later the "sleep" score changed to 1, the state will change to `{'heart': 3, 'sleep': 1}` and remain a severity of 3 since severity is calculated as the max score within state. If later the "heart" score changed to 1, the resultant state would be `{'heart': 1, 'sleep': 1}` and the severity would drop to 1 indicating an overall "good" health.

Defining a derived `Health` model called `BodyHealth` is as simple as the following.

    models.py::

        from health_monitor.models import Health


        class BodyHealth(Health):
            pass


`HealthTest`
------------

The base `HealthTest` model serves the purpose of storing historical test results, turning raw test results into normalized scores, and automatically updating the overall health. For this example, let us define two health tests - `HeartHealthTest` and `SleepHealthTest`.

    models.py::

        from django.db import models

        from health_monitor.models import HealthTest


        class HeartHealthTest(HealthTest):
            heartrate = models.IntegerField()

            health_model = BodyHealth
            groups = ['doctor']
            test = 'heart'

            @staticmethod
            def score(heartrate):
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
            hours = models.FloatField()

            health_model = BodyHealth
            groups = ['doctor']
            test = 'sleep'

            @staticmethod
            def score(hours):
                hours = float(hours)

                if sleep < 4:
                    return 4
                elif sleep < 6:
                    return 3
                elif sleep < 8:
                    return 2
                else:
                    return 1

When defining derived `HealthTest` models such as `HeartHealthTest` and `SleepHealthTest`, there are three attributes that are required - `health_model`, `groups`, and `test`.

- `health_model` is an association to the model that holds the states (defined above)
- `groups` is a list of user-defined groups that each test will be associated with and there must be at minimum one group in order for test results to update the "health state"
- `test` is a string that will be used to reference the test in the API (following section)

Additionally, a static method for `score` is used to interpret raw test result values and normalize and return a "health score".

Note:

- The inputs for the `score` method should be type-converted to the correct type (int, float, char, etc.) to clean data that is passed incorrectly.
- The `score` method also must return an integer score otherwise it will fail.

****************
2. Configure API
****************

The following steps create an API with the following endpoints and actions:

- /health/
    - GET a list of all health uids
- /health/<uid>/
    - GET the health of a particular uid
    - DELETE the health for a particular uid
- /health/<uid>/<group>/
    - GET the health of a particular uid and group
    - DELETE health of a particular uid and group
- /health/<uid>/<group>/<test>/
    - GET the health of a particular uid and group and test
    - DELETE the health of a particular uid and group and test
- /health_test/
    - GET a list of all health tests
- /health_tests/<test>/?uids=<uids>&start_time=<start_time>&end_time=<end_time>
    - GET test results for a particular test with filters
- /health_test/<test>/<uid>/?start_time=<start_time>&end_time=<end_time>
    - GET test results for a particular test and uid with filters
- /health_test/<test>/<uid>/
    - POST test results for a particular test and uid


Where:

- <uid> is a unique identifier of an asset.
- <group> is the name of a group of tests.
- <test> is the name of a health test.

And query string arguments:

- <uids> - a comma separated list of uids
- <start_time> - a datetime string in ISO 8601 format (optional)
- <end_time> - a datetime string in  ISO 8601 format (optional)
- example: /health/heart/?uids=1,2,3&start_time=xxx&end_time=xxx

Configure `HealthView` and `HealthTestView` Models
--------------------------------------------------
The following class definitions should be made to configure the API view classes.

    views.py::

        from health_monitor.views import HealthTestView, HealthView

        from .models import BodyHealth


        class BodyHealthView(HealthView):
            health_model = BodyHealth


        class BodyHealthTestView(HealthTestView):
            pass

Where `health_model` is set to the `Health` model defined above.

Map URLs to Views
-----------------
The following url definitions should be made to enable all of the endpoints and actions described above.

    urls.py::


        from django.conf.urls import url

        from . import views


        urlpatterns = [
            url(r'^health/$', views.BodyHealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/$', views.BodyHealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/(?P<group>[\w]*)/$', views.BodyHealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/(?P<group>[\w]*)/(?P<test>[\w]*)/$', views.BodyHealthView.as_view()),
            url(r'^health_test/$', views.BodyHealthTestView.as_view()),
            url(r'^health_test/(?P<test>[\w-]*)/$', views.BodyHealthTestView.as_view()),
            url(r'^health_test/(?P<test>[\w-]*)/(?P<uid>[\d]*)/$', views.BodyHealthTestView.as_view()),
        ]

In this example, `BodyHealthView` and `BodyHealthTestView` are the names of the View models that we defined in the previous section.


*********************************
3. Customize Notification Filters
*********************************
TODO
