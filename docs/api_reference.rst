#############
API Reference
#############

This is a quick reference to API endpoints that are available after configuring Django Health Monitor in a Django project. For a full explanation of configuring and using Django Health Monitor, see `Usage <usage.html>`_.

******
Health
******

The following endpoints and actions describe the behavior of models derived from the `Health` model, which store the 'health state', 'health severity', and cached 'health history'.

.. include:: api/health.rst


***********
Health Test
***********

The following endpoints and actions describe the behavior of models derived from the `HealthTest` model, which store test results.

.. include:: api/health_test.rst


************
Health Alarm
************

The following endpoints and actions describe the behavior of models derived from the `HealthAlarm` model, which calculates which assets in a 'population' or 'system' exhibit elevated status based on four filters - score, aggregate_percent, repetition, repetition_percent.

.. include:: api/health_alarm.rst
