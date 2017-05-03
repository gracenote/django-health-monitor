=============================
Django Health Monitor
=============================

.. image:: https://img.shields.io/pypi/l/django-health-monitor.svg
    :target: https://pypi.python.org/pypi/django-health-monitor

.. image:: https://img.shields.io/pypi/pyversions/django-health-monitor.svg
    :target: https://pypi.python.org/pypi/django-health-monitor

.. image:: https://badge.fury.io/py/django-health-monitor.png
    :target: https://badge.fury.io/py/django-health-monitor

.. image:: https://travis-ci.org/gracenote/django-health-monitor.png?branch=master
    :target: https://travis-ci.org/gracenote/django-health-monitor

.. image:: https://img.shields.io/codecov/c/github/gracenote/django-health-monitor/master.svg
    :target: https://codecov.io/gh/gracenote/django-health-monitor

A Django application to help track the health of assets within a "system" or "population" and give real-time feedback.

Background
----------

This project was born from a need to quickly identify system problems across production applications. Monitoring scripts were run in Jenkins and the number of emails generated reporting problems quickly became unmanageable, which resulted in the underlying logic in this application.

This application was created in an effort to represent a general model where assets with unique identifiers (uids) are being monitored repeatedly, and it is necessary to see elevated states on an individual basis, but more importantly on a "system"-wide or "population"-wide basis.

Documentation
-------------

The full documentation is at https://django-health-monitor.readthedocs.org.

Quickstart
----------

django-health-monitor is available on `PyPI <https://pypi.python.org/pypi/django-health-monitor>`_ and can be installed using pip::

    $ pip install django-health-monitor

After installing, add ``'health_monitor'`` to ``INSTALLED_APPS`` in ``settings.py``.

Features
--------

- Configurable scoring logic that translates raw test results to normalized "health scores".
- API endpoints that allow monitoring scripts to post test results based on a test name, unique identifier of an asset, and test results. Posting a test result also updates the asset's "health state score", "health severity score", and "health score history" for faster alert calculations.
- API endpoints for retrieving historical test results of an asset.
- API endpoints for retrieving an asset's current health metrics - state scores, severity scores, and score history.
- API endpoints that identify assets within a "system" or "population" that exhibit elevated health states based off of four criteria - score, aggregate percent, repetition, and repetition percent.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

There were many people involved in creating  this application that were not involved with the coding, but deserve a bulk of the credit. They helped design the application's underlying logic, and continually used it and recommended new ways to quickly extract insight. They will not be named specifically, but their help was invaluable.

Thank you `Gracenote <http://www.gracenote.com/>`_ for encouraging involvement in open-source projects.

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
