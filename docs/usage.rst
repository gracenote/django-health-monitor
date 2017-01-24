========
Usage
========

To use Django Health Monitor in a project, there are three main steps:

1. Set up API endpoint to handle test result updates.
2. Create scoring logic to give test results relative weighting of significance.
3. Customize notification filters. (optional)


Set Up API
----------

The following steps with create an API with the following endpoints, where <uid>
is a unique identifier for the asset that is being tracked. The unique identifier
must be an integer. The <subscriber> tag is a required attribute that must be attached
to a test, and this will be described in the next section.

<start_time> and <end_time> must be passed in the format ``'%Y-%m-%d %H:%M:%S'``.

health/<uid>/read/
health/<uid>/history/<subscriber>/?start_time=<start_time>&end_time=<end_time>
health/<uid>/update/


1. Create a new application using the command ``django-admin startapp health``.

Inside of the newly created ``health`` application, modify ``models.py`` adding
the following model::

    import health_monitor


    class Health(health_monitor.models.Health):
        pass
