=====
Usage
=====

To use Django Health Monitor in a project, there are three main steps:

1. Configure API to handle test result updates.
2. Configure scoring logic to give test results relative weighting of significance.
3. Customize notification filters. (optional)

****************
1. Configure API
****************

The following steps create an API with the following endpoints:

- /health/
- /health/<uid>/
- /health/<uid>/<test>/

Where:

- <uid> is a unique identifier for the asset that is being tracked.
- <test> is the name of a test associated with the asset. Scoring logic (below) will need to be configured before test scores can be posted to an asset.


Create Health Models
--------------------
    models.py::

        from health_monitor.models import Health

        class HeartHealth(Health):
            pass


Create Health Views
-------------------
    views.py::

        from health_monitor.views import HealthView

        class HearthHealthView(HealthView):
            pass

Map URLs to Views
-----------------
    urls.py::


        from django.conf.urls import url
        from views import HeartHealthView

        urlpatterns = [
            url(r'^health/$', HeartHealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/$', HeartHealthView.as_view()),
            url(r'^health/(?P<uid>[\w]*)/(?P<test>[\w]*)/$', HeartHealthView.as_view()),
        ]


Configure Scoring Logic
-----------------------

TODO


Customize Notification Filters
------------------------------

TODO
