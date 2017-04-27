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

Two main types of models are needed to track a system's state and to capture test results - `Health` and `HealthTest`. For these examples, we will put the `Health` and the `HealthTest` related model and views into the application `health`.

The application can be created with the command::

    django-admin startapp health

`Health`
--------

The base `Health` model serves the purpose of storing an asset's latest "health test" results from a variety tests, normalized as test "scores" in a "health state". Additionally, the highest result from the normalized test scores equals an asset's "health severity", which is used to quickly highlight which assets have an elevated status and should be investigated.

To explain this concept, let's say that an overall `BodyHealth` depends on a "heart" test result and a "sleep" test result, each of which have four normalized test scores - 1 for good, 2 for mildly bad, 3 for moderately bad, and 4 for extremely bad. For a particular person, a "heart" score of 3 and a "sleep" score of 2 would result in a state of `{'heart': 3, 'sleep': 2}` and a severity of 3. If later the "sleep" score changed to 1, the state will change to `{'heart': 3, 'sleep': 1}` and remain a severity of 3 since severity is calculated as the max score within state. If later the "heart" score changed to 1, the resultant state would be `{'heart': 1, 'sleep': 1}` and the severity would drop to 1 indicating an overall "good" health.

Defining a derived `Health` model called `BodyHealth` is as simple as the following.

    health/models.py::

        from health_monitor.models import Health


        class BodyHealth(Health):
            pass


`HealthTest`
------------

The base `HealthTest` model serves the purpose of storing historical test results, turning raw test results into normalized scores, and automatically updating the overall health. For this example, let us define two health tests - `HeartHealthTest` and `SleepHealthTest`.

    health/models.py::

        from django.db import models
        from health_monitor.models import Health, HealthTest


        class BodyHealth(Health):
            pass


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
            groups = ['doctor', 'coach']
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

.. note::
    - The inputs for the `score` method should be type-converted to the correct type (int, float, char, etc.) to clean data that is passed incorrectly.
    - The `score` method also must return an integer score otherwise it will fail.

****************
2. Configure API
****************

API Endpoints
-------------

The following steps create an API with the following endpoints and actions:

- /health/
    - GET a list of all health uids
- /health/<uid>/
    - GET the health of a particular uid
    - DELETE the health of a particular uid
- /health/<uid>/<group>/
    - GET the health of a particular uid and group
    - DELETE health of a particular uid and group
- /health/<uid>/<group>/<test>/
    - GET the health of a particular uid and group and test
    - DELETE the health of a particular uid and group and test
- /health_test/
    - GET a list of all health tests
- /health_tests/<test>/?uids=<uids>&start_time=<start_time>&end_time=<end_time>
    - GET test results of a particular test with filters
- /health_test/<test>/<uid>/?start_time=<start_time>&end_time=<end_time>
    - GET test results of a particular test and uid with filters
- /health_test/<test>/<uid>/
    - POST test results of a particular test and uid


Where:

- <uid> is a unique identifier of an asset.
- <group> is the name of a group of tests.
- <test> is the name of a health test.

And query string arguments:

- <uids> - a comma separated list of uids
- <start_time> - a datetime string in ISO 8601 format (optional)
- <end_time> - a datetime string in  ISO 8601 format (optional)
- example: /health/heart/?uids=1,2,3&start_time=xxx&end_time=xxx

Configure `HealthView` and `HealthTestView` Views
-------------------------------------------------
The following class definitions should be made to configure the API view classes.

    health/views.py::

        from health_monitor.views import HealthTestView, HealthView

        from .models import BodyHealth


        class BodyHealthView(HealthView):
            health_model = BodyHealth


        class BodyHealthTestView(HealthTestView):
            pass

Where `health_model` is set to the `Health` model defined above.

.. note::
    - By default, to post 'health test' results, a CSRF token will need to be passed in the Header in the form `{X-CSRFTOKEN: <token>}` where `<token>` is the CSRF token. More information can be found in this `Stack Overflow discussion <http://stackoverflow.com/questions/13567507/passing-csrftoken-with-python-requests>`_.
    - Alternately, the `HealthTest` view can be overwritten to CSRF exempt, which will allow 'health test' results to be posted without a CSRF token in the header by modifying the view from above as the following.

    health/views.py::

        from django.utils.decorators import method_decorator
        from django.views.decorators.csrf import csrf_exempt


        class BodyHealthTestView(HealthTestView):
            @method_decorator(csrf_exempt)
            def dispatch(self, request, *args, **kwargs):
                return super(BodyHealthTestView, self).dispatch(request, *args, **kwargs)

Map URLs to Views
-----------------
The following url definitions should be made to enable all of the endpoints and actions described above.

    <project>/urls.py::


        from django.conf.urls import url

        from health import views


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

Test API
--------

At this point, there should be a working API that will store raw 'health test' results as well as generating a normalized 'health' state. Let's try some sample calls to see how the API works. For these examples we will be using the Python `Requests <http://docs.python-requests.org/en/master/>`_ package and will run the Django project locally. For these examples, CSRF checks have been disabled for clarity.

    Initially, our `BodyHealth`, `HeartHealthTest`, and `SleepHealthTest` models are empty. We can see that navigating to `/health/` shows us that no health states exist and that navigating to `/health_test/` shows that two tests have been configured 'heart' and 'sleep'::

        In [1]: import requests
        In [2]: r = requests.get('http://localhost:8000/health/')
        In [3]: r.json()
        Out[3]: {u'uids': []}
        In [4]: r = requests.get('http://localhost:8000/health_test/')
        In [5]: r.json()
        Out[5]: {u'tests': [u'heart', u'sleep']}

    Let's post a 'heart' test result where 'heartrate' equals 60 for an asset with a `uid` of 1 and see what happens::

        In [6]: r = requests.post('http://localhost:8000/health_test/heart/1/', data={'heartrate': 60})
        In [7]: r.json()
        Out[7]: {u'message': u'heart score changed to 1 for uid 1', u'score': 1}
        In [8]: r = requests.get('http://localhost:8000/health_test/heart/1/')
        In [9]: r.json()
        Out[9]: [{u'heartrate': 60, u'time': u'2017-04-27T19:08:04.381651+00:00', u'uid': 1}]
        In [10]: r = requests.get('http://localhost:8000/health/')
        In [11]: r.json()
        Out[11]: {u'uids': [1]}
        In [12]: r = requests.get('http://localhost:8000/health/1/')
        In [13]: r.json()
        Out[13]:
        {
            u'severity': {
                u'doctor': {u'score': 1, u'updated': u'2017-04-27T19:08:04.385Z'}
            },
            u'state': {
                u'doctor': {
                    u'heart': {u'score': 1, u'updated': u'2017-04-27T19:08:04.385Z'}
                }
            },
            u'uid': 1
        }

    At this point, we can see that:
        - On lines 6 and 7, we received a response for our post indicating that the score was changed to 1. (Recall that from our model definition, a heartrate of 80 or below results in a `score` of 1).
        - On lines 8 and 9, we can see the history of heart tests for `uid` 1.
        - On lines 10 and 11, we can see that there is now a `health` instance generated for `uid` 1.
        - On lines 12 and 13, we can see that the resulting `health` instance has `state` and `severity` entries for the group 'doctor'. (Recall that from our model definition, the 'heart' test belongs to the `group` 'doctor'.

    Now let's post a 'sleep' test result where 'hours' equals 5.0 for the same asset with `uid` of 1 and see what happens::

        In [14]: r = requests.post('http://localhost:8000/health_test/sleep/1/', data={'hours': 5.0})
        In [15]: r.json()
        Out[15]: {u'message': u'sleep score changed to 3 for uid 1', u'score': 3}
        In [16]: r = requests.get('http://localhost:8000/health/1/')
        In [17]: r.json()
        Out[17]:
        {
            u'severity': {
                u'coach': {u'score': 3, u'updated': u'2017-04-27T19:18:00.654Z'},
                u'doctor': {u'score': 3, u'updated': u'2017-04-27T19:18:00.654Z'}
            },
            u'state': {
                u'coach': {
                    u'sleep': {u'score': 3, u'updated': u'2017-04-27T19:18:00.654Z'}
                },
                u'doctor': {
                    u'heart': {u'score': 1, u'updated': u'2017-04-27T19:08:04.385Z'},
                    u'sleep': {u'score': 3, u'updated': u'2017-04-27T19:18:00.654Z'}
                }
            },
            u'uid': 1
        }

    Now, we can see that:
        - On lines 14 and 15, we received a response for our post indicating that the score was changed to 3. (See above model definition for sleep scoring criteria.)
        - On lines 16 and 17, we now have additional `state` and `severity` entries for the `group` coach since the sleep test belongs to the `groups` 'doctor' and 'coach'. The `score` for the sleep test has been added in both `state` groups and the `severity` has been updated to 3 for both groups since the `severity score` is calculated as the maximum of all `state scores`.

*********************************
3. Customize Notification Filters
*********************************
TODO
