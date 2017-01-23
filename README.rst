=============================
Django Health Monitor
=============================

.. image:: https://badge.fury.io/py/django-health-monitor.png
    :target: https://badge.fury.io/py/django-health-monitor

.. image:: https://travis-ci.org/seanchon/django-health-monitor.png?branch=master
    :target: https://travis-ci.org/seanchon/django-health-monitor

A Django app to help track the health of a system and give real-time feedback. (CURRENTLY IN DEVELOPMENT)

The application consists of the following components:

- An API endpoint that allows monitoring scripts to update test results to a unique identifier of an asset.
- API endpoints for retrieving historical result of an asset.
- A notification engine allowing customized notifications based on test results.

Documentation
-------------

The full documentation is at https://django-health-monitor.readthedocs.org.

Quickstart
----------

Install Django Health Monitor::

    pip install django-health-monitor

Then use it in a project::

    import health_monitor

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
