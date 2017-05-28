#####
Usage
#####

To use Django Health Monitor in an application, there are three main steps:

1. Define Models
2. Configure API
3. Configure Health Alarm (optional)


****************
1. Define Models
****************

Two main types of models are needed to track a system's state and to capture test results - `Health` and `HealthTest`. For these examples, we will put the `Health` and the `HealthTest` related model and views into the application `health`.

The application can be created with the command::

    django-admin startapp health

Make sure to add ``'health'`` to ``INSTALLED_APPS`` in ``settings.py`` if you are following along with this example.

`Health`
--------

The base `Health` model serves the purpose of storing an asset's latest `health test` results from a variety tests, normalized as test `scores` in a `health state`. Additionally, the highest result from the normalized test scores equals an asset's `health severity`, which is used to quickly highlight which assets have an elevated status and should be investigated.

To explain this concept, let's say that an overall `BodyHealth` depends on a 'heart' test result and a 'sleep' test result, each of which have four normalized test scores - 1 for good, 2 for mildly bad, 3 for moderately bad, and 4 for extremely bad. For a particular person, a 'heart' score of 3 and a 'sleep' score of 2 would result in a state of `{'heart': 3, 'sleep': 2}` and a severity of 3. If later the 'sleep' score changed to 1, the state will change to `{'heart': 3, 'sleep': 1}` and remain a severity of 3 since severity is calculated as the max score within state. If later the 'heart' score changed to 1, the resultant state would be `{'heart': 1, 'sleep': 1}` and the severity would drop to 1 indicating an overall "good" health.

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
            def score(heartrate, **kwargs):
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
            def score(hours, **kwargs):
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
- `groups` is a list of user-defined groups that each test will be associated with and there must be at minimum one group in order for test results to update the `health state`
- `test` is a string that will be used to reference the test in the API (following section)

Additionally, a static method for `score` is used to interpret raw test result values and normalize and return a `health score`.

.. note::
    - The definition of score must include an input for `**kwargs`.
    - The inputs for the `score` method should be type-converted to the correct type (int, float, char, etc.) to clean data that is passed incorrectly.
    - The `score` method also must return an integer score otherwise it will fail.
    - Additional attributes may be added to HealthTest models to store values that are not used in current score calculations, but may be used for score calculations at a later time.

****************
2. Configure API
****************

API Endpoints for `Health` and `HealthTest` Models
--------------------------------------------------

The following steps create an API with the following endpoints and actions:

**health**

.. include:: api/health.rst

**health_test**

.. include:: api/health_test.rst

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
        from health_monitor.views import HealthTestView, HealthView

        from .models import BodyHealth


        class BodyHealthView(HealthView):
            health_model = BodyHealth

            @method_decorator(csrf_exempt)
            def dispatch(self, request, *args, **kwargs):
                return super(BodyHealthView, self).dispatch(request, *args, **kwargs)


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

Test the API
------------

At this point, there should be a working API that will store raw 'health test' results as well as generating a normalized 'health' state. Let's try some sample calls to see how the API works. For these examples we will be using the Python `Requests <http://docs.python-requests.org/en/master/>`_ package and will run the Django project locally. For these examples, CSRF checks have been disabled for clarity.

    Initially, our `BodyHealth`, `HeartHealthTest`, and `SleepHealthTest` models are empty. We can see that navigating to `/health/` shows us that no health states exist and that navigating to `/health_test/` shows that two tests have been configured 'heart' and 'sleep'::

        In [1]: import requests
        In [2]: r = requests.get('http://localhost:8000/health/')
        In [3]: r.json()
        Out[3]: {u'uids': []}
        In [4]: r = requests.get('http://localhost:8000/health_test/')
        In [5]: r.json()
        Out[5]: {u'tests': [u'heart', u'sleep']}

    Let's post a 'heart' test result where 'heartrate' equals 90 for an asset with a `uid` of 1 and see what happens::

        In [6]: r = requests.post('http://localhost:8000/health_test/heart/1/', data={'heartrate': 90})
        In [7]: r.json()
        Out[7]: {u'message': u'heart score changed to 2 for uid 1', u'score': 2}
        In [8]: r = requests.get('http://localhost:8000/health_test/heart/1/')
        In [9]: r.json()
        Out[9]: [{u'heartrate': 90, u'score': 2, u'time': u'2017-04-27T20:47:34.594848+00:00', u'uid': 1}]
        In [10]: r = requests.get('http://localhost:8000/health/')
        In [11]: r.json()
        Out[11]: [1]
        In [12]: r = requests.get('http://localhost:8000/health/1/')
        In [13]: r.json()
        Out[13]:
        {
            u'severity': {
                u'doctor': {u'score': 2, u'updated': u'2017-04-27T20:47:34.597Z'}
            },
            u'state': {
                u'doctor': {
                    u'heart': {u'score': 2, u'updated': u'2017-04-27T20:47:34.597Z'}
                }
            },
            u'uid': 1
        }

    At this point, we can see that:
        - On lines 6 and 7, we received a response for our post indicating that the score was changed to 2. (Recall that from our model definition, a 'heartrate' between 81 and 100 results in a `score` of 2).
        - On lines 8 and 9, the history of 'heart' tests for `uid` 1 is now visible.
        - On lines 10 and 11, there is now a `health` instance generated for `uid` 1.
        - On lines 12 and 13, the resulting `health` instance has `state` and `severity` entries for the group 'doctor' with `scores` of 2 for both. (Recall that from our model definition, the 'heart' test belongs to the `group` 'doctor'.

    Now let's post a 'sleep' test result where 'hours' equals 8.0 for the same asset with `uid` of 1 and see what happens::

        In [14]: r = requests.post('http://localhost:8000/health_test/sleep/1/', data={'hours': 8.0})
        In [15]: r.json()
        Out[15]: {u'message': u'sleep score changed to 1 for uid 1', u'score': 1}
        In [16]: r = requests.get('http://localhost:8000/health/1/')
        In [17]: r.json()
        Out[17]:
        {
            u'severity': {
                u'coach': {u'score': 1, u'updated': u'2017-04-27T20:51:31.674Z'},
                u'doctor': {u'score': 2, u'updated': u'2017-04-27T20:47:34.597Z'}
            },
            u'state': {
                u'coach': {
                    u'sleep': {u'score': 1, u'updated': u'2017-04-27T20:51:31.674Z'}
                },
                u'doctor': {
                    u'heart': {u'score': 2, u'updated': u'2017-04-27T20:47:34.597Z'},
                    u'sleep': {u'score': 1, u'updated': u'2017-04-27T20:51:31.673Z'}
                }
            },
            u'uid': 1
        }

    Now, we can see that:
        - On lines 14 and 15, we received a response for our post indicating that the score was changed to 1. (See above model definition for sleep scoring criteria.)
        - On lines 16 and 17, we now have additional `state` and `severity` entries for the `group` 'coach' since the sleep test belongs to the `groups` 'doctor' and 'coach'. The `state` for both groups has been updated to include the sleep score, however, only the `severity score` for 'coach' has been set to 1 and the `severity score` for 'doctor' remains set to 2 since `severity` is calculated as the maximum of all of the `state scores`.

    Finally, let's try a delete on this `health` instance. This is often useful if an entire test is deprecated, a `group` is removed, or a `uid` is removed from a test run since the `health` will persist unless deleted. Let's see what happens::

        In [18]: r = requests.delete('http://localhost:8000/health/1/doctor/heart/')
        In [19]: r.json()
        Out[19]: {u'message': u'heart test deleted from doctor group in 1 health'}
        In [20]: r = requests.get('http://localhost:8000/health/1/')
        In [21]: r.json()
        Out[21]:
        {
            u'severity': {
                u'coach': {u'score': 1, u'updated': u'2017-04-27T20:55:06.311Z'},
                u'doctor': {u'score': 1, u'updated': u'2017-04-27T21:24:44.047Z'}
            },
            u'state': {
                u'coach': {
                    u'sleep': {u'score': 1, u'updated': u'2017-04-27T20:55:06.311Z'}
                },
                u'doctor': {
                    u'sleep': {u'score': 1, u'updated': u'2017-04-27T20:55:06.311Z'}
                }
            },
            u'uid': 1
        }

    We see that:
        - On lines 18 and 19, we received a response that the 'heart' `health test` was deleted from the 'doctor' `group` in 1's `health`.
        - On lines 20 and 21, the `health state` was updated with the removal of the 'heart' `health test` and the `severity` for the 'doctor' `group` was updated accordingly.

*************************
3. Configure Health Alarm
*************************

API Endpoints for `HealthAlarm` Model
-------------------------------------

Setting up "Health Alarms" within Django Health Monitor is meant to identify alerts for issues that affect a certain portion of a system or population. Whenever a test result for an "asset" (e.g. a person, a server, a stock ticker, etc.) is written, the resulting write updates the asset's health state, health severity, and health history, which help to quickly identify issues that are affecting a portion of a system or population.

The following steps create an API that allow us to filter which assets within a system or population exhibit failure conditions based off of four criteria - score, aggregate percent, repetition, and repetition percent - using an API with the following endpoints and actions:

**health_alarm**

.. include:: api/health_alarm.rst

Let's illustrate this concept with an example. Let's say the following test results have been recorded for assets with <uids> of 1, 2, and 3 at times t1, t2, t3, t4, and t5.

    heartrate results::

           t1   t2   t3   t4   t5
        1: 61,  63,  81,  69,  62
        2: 65,  94,  115, 112, 110
        3: 119, 110, 111,  94, 59


    Let's recall the `score` criteria defined earlier::

        if heartrate > 120:
            return 4
        elif heartrate > 100:
            return 3
        elif heartrate > 80:
            return 2
        else:
            return 1

    The normalized results then become::

          t1 t2 t3 t4 t5
        1: 1, 1, 2, 1, 1
        2: 1, 2, 3, 3, 3
        3: 3, 3, 3, 2, 1

Let's look at some example responses if we were to pass different query strings at different times:

    - @t1: GET /health_alarm/doctor/heart/?score=2
        - returns `[3]`.
    - @t1: GET /health_alarm/doctor/heart/?score=2&aggregate_percent=50
        - returns `[]` since only 1/3 assets exhibit a failure condition.
    - @t3: GET /health_alarm/doctor/heart/?score=2&repetition=2
        - returns `[2, 3]` since @t2, the health score for `uid` 1 is 1 and is therefore in a pass state.
    - @t5: GET /health_alarm/doctor/heart/?score=2&repetition=3&repetition_percent=25
        - returns `[1, 2, 3]` since all three assets have a failure rate higher than 25% from t3 to t5.
    - @t5: GET /health_alarm/doctor/heart/?score=2&repetition=3
        - returns `[2]`

These four "levers" - `score`, `aggregate_percent`, `repetition`, and `repetition_percent` - are meant to help make tests less sensitive to small system-wide failures (raising `aggregate_percent`), less sensitive to failure "blips" that automatically correct themselves (increasing `repetition`), more sensitive to failures within a sequence of tests (lowering `repetition_percent`), etc.

Configure `HealthAlarm` Model
-----------------------------

Now that we have discussed the general overview of how alarms work, if you are interested in setting them up, read on! In order to enable health alarms, a derived `HealthAlarm` model will need to be defined, which will point to the derived `Health` model defined above. For our example, we will use the `BodyHealth` model defined earlier and call the new derived `HealthAlarm` model `BodyHealthAlarm`.

    health/models.py::

        from health_monitor.models import HealthAlarm


        class BodyHealthAlarm(HealthAlarm):
            health_model = BodyHealth

If following the example from previous sections, the new `models.py` file will look similar to the following with the `HealthTest` model details omitted.

    health/models.py::

        from django.db import models

        from health_monitor.models import Health, HealthAlarm, HealthTest


        class BodyHealth(Health):
            pass


        class BodyHealthAlarm(HealthAlarm):
            health_model = BodyHealth


        class HeartHealthTest(HealthTest):
            ...


        class SleepHealthTest(HealthTest):
            ...

Configure `HealthAlarmView` View
--------------------------------

In order to configure the view, which will later be referenced by the API configuration in the next section, we will simply set up the following making sure to set the `health_alarm_model` to point to `BodyHealthAlarm`, which was defined in the previous section.

    health/views.py::

        from health_monitor.views import HealthAlarmView

        class BodyHealthAlarmView(HealthAlarmView):
            health_alarm_model = BodyHealthAlarm

In totality, the views we have defined in this example should look like the following.

    health/views::

        from health_monitor.views import HealthTestView, HealthAlarmView, HealthView

        from .models import BodyHealth, BodyHealthAlarm


        class BodyHealthView(HealthView):
            health_model = BodyHealth


        class BodyHealthAlarmView(HealthAlarmView):
            health_alarm_model = BodyHealthAlarm

        class BodyHealthTestView(HealthTestView):
            pass

Configure `HealthAlarm` API Endpoints
-------------------------------------

Finally, we can create urls to point to the `HealthAlarmView` created in the previous section.

    health/urls.py::

        from django.conf.urls import url

        from . import views


        urlpatterns = [
            url(r'^health_alarm/$', views.BodyHealthAlarmView.as_view()),
            url(r'^health_alarm/(?P<group>[\w]*)/$', views.BodyHealthAlarmView.as_view()),
            url(r'^health_alarm/(?P<group>[\w]*)/(?P<test>[\w]*)/$', views.BodyHealthAlarmView.as_view()),
        ]

And if you have been following along from the beginning, all of the API end points for health, health_test, and health_alarm actions are as follows.

    health/urls.py::

        from django.conf.urls import url

        from . import views


        urlpatterns = [
            url(r'^health/$', views.BodyHealthView.as_view()),
            url(r'^health/(?P<uid>[\d]*)/$', views.BodyHealthView.as_view()),
            url(r'^health/(?P<uid>[\d]*)/(?P<group>[\w]*)/$', views.BodyHealthView.as_view()),
            url(r'^health/(?P<uid>[\d]*)/(?P<group>[\w]*)/(?P<test>[\w]*)/$', views.BodyHealthView.as_view()),
            url(r'^health_test/$', views.BodyHealthTestView.as_view()),
            url(r'^health_test/(?P<test>[\w]*)/$', views.BodyHealthTestView.as_view()),
            url(r'^health_test/(?P<test>[\w]*)/(?P<uid>[\d]*)/$', views.BodyHealthTestView.as_view()),
            url(r'^health_alarm/$', views.BodyHealthAlarmView.as_view()),
            url(r'^health_alarm/(?P<group>[\w]*)/$', views.BodyHealthAlarmView.as_view()),
            url(r'^health_alarm/(?P<group>[\w]*)/(?P<test>[\w]*)/$', views.BodyHealthAlarmView.as_view()),
        ]
