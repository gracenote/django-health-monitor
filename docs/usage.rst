========
Usage
========

To use Django Health Monitor in a project, there are three main steps:

1. Set up API endpoint to handle test result updates.
2. Configure scoring logic to give test results relative weighting of significance.
3. Customize notification filters. (optional)


Set Up API
----------

The following steps with create an API with the following endpoints:

- health/<uid>/
- health/<uid>/update/<test_name>/?<params>
- health/<uid>/history/<subscriber>/?start_time=<start_time>&end_time=<end_time>


- <uid> is a unique identifier for the asset that is being tracked. The unique identifier must be an integer.
- <test_name> is the name of a scoring logic test. Implementation will be described in the following section.
- <subscriber> is a required attribute that must be attached to scoring logic allowing unique suites of tests. Implementation will be described in the following section.
- The <start_time> and <end_time> are time filters and must be passed in UTC and in the format ``'%Y-%m-%dT%H:%M:%SZ'``.


1. Run ``python manage.py migrate health_monitor`` to create a new table to track health instances.


2. Add url routes. Inside of ``urls.py`` add the following routes::

    from health_monitor import views as health_monitor_views

    urlpatterns = [
        ...
        url(r'^health/(?P<uid>[\w-]*)/$', health_monitor_views.read, name='read'),
        url(r'^health/(?P<uid>[\w-]*)/history/(?P<subscriber>[\w-]*)/$', health_monitor_views.history, name='history'),
        url(r'^health/(?P<uid>[\w-]*)/update/(?P<test_name>[\w-]*)/$', health_monitor_views.update, name='update'),
        ...
    ]


Configure Scoring Logic
-----------------------

TODO


Customize Notification Filters
------------------------------

TODO
