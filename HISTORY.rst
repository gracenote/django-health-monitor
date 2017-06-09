.. :changelog:

History
-------


0.2.8 (2017-06-09)
++++++++++++++++++

* Update docs.
* Change Travis CI coverage to officially supported combinations of Django and Python. https://docs.djangoproject.com/en/1.11/faq/install/#what-python-version-can-i-use-with-django
* Add class method ‘get_or_create’ to Health model to address bug when upgrading to Django 1.11.2. (#2)
* Add Travis CI coverage for Django 1.11.
* Update docs.
* Add CI coverage for Python 3.6.
* Refactor HealthTestView ‘get’ method to reduce number of function calls.

0.2.7 (2017-05-24)
++++++++++++++++++

* Make ‘uids’ an optional parameter when getting test result history.

0.2.6 (2017-05-22)
++++++++++++++++++

* Update docs.
* Return ‘groups’ for API view /health_alarm/.
* Fix logic to selectively scan repetition history for repetition_percent = 100.
* Fix logic to selectively scan repetition history for repetition_percent = 100.
* Update changelog history.
* Update docs.

0.2.5 (2017-05-10)
++++++++++++++++++

* Publish 0.2.5.
* Update health/ view to accept query-string boolean argument ‘detail’ to return health details.
* Update docs.
* Update docs.
* Update docs.
* Add query string param to get latest result from health_test search.
* Fix link to Usage page.
* Fix indentation.
* Add API reference page.
* Split health and health_test snippets.
* Use doc snippets.
* Update version.
* Fix bug with import error in production environment.

0.2.4 (2017-05-08)
++++++++++++++++++

* Publish 0.2.4.
* Move cleansing of string to bool to utils.
* Change post response to return score from get_score method.


0.2.3 (2017-05-05)
++++++++++++++++++

* Publish 0.2.3.
* Add docstring explanation.
* Add type conversion of BooleanFields to fix request.POST passing string values of 0, False, etc.
* Update Sphinx config.

0.2.2 (2017-05-04)
++++++++++++++++++

* Publish 0.2.2.
* Add util for response.content to json.
* Use json.loads(response.content) since Django<1.9 does not support response.content.json().
* Update docs.
* Return score in health test history.
* Update docs.
* Update README.rst
* Update docs.
* Update docs.
* Update docs.
* Update docs.

0.2.1 (2017-05-01)
++++++++++++++++++

* Publish 0.2.1.
* Add HealthAlarm views and url endpoints.
* Update docstrings.
* Add HealthAlarm model and related methods to enable calculation of alarms.
* Update docs.
* Update docs.
* Add Health history cache and method for get_history.
* Add get_score method for HealthTest instance.
* Update docs.
* Merge branch 'documentation'
* Update docs.
* Update uids in urls to digits.
* Update docs.

0.2.0 (2017-04-26)
++++++++++++++++++

* Publish 0.2.0.
* Update docs.
* Update docs.
* Update docs.
* Update docs.
* Update docs.
* Update docs.
* Update requirements, license, and Django 1.11.
* Decode response.content.
* Add util to convert response.content to a dict in python3.
* Modify config to install requirement.txt.
* Change to minimum requirements.
* Add pytz to requirements.
* Enable Travis CI on dev branch.
* Update docs.
* Exception handle for negative scores.
* Add DELETE action for /health/<uid>/<group>/<test>/.
* Add DELETE action for /health/<uid>/<group>/.
* Rename delete_test_state() to delete_test().
* Add views for GET /health/<uid>/<group>/ and GET /health/<uid>/<group>/<test>/.
* Add test for GET /health/.
* Comment on `naive datetime` warning.
* Reorder tests and add comments.
* Modify test to to pass query-string times with and without UTC offset.
* Add handling of ISO 8601 timezone offset.
* Add pip package python-dateutil for handling of url dates.
* Update docs.
* Add API view for health test historical results.
* Add view for /health_test/ index.
* Create separate HealthTestView to handle HealthTest related actions.
* Fix naive datetime warning.
* Change order of methods.
* Change POST response message.
* Change name of history method to get_history.
* Add history class method to filter by uids, start_time, and end_time.
* Change _get_tests to static method.
* Add time column to test results.
* Fix health test inserts.
* Change uid to integer.
* Change uid to integer.
* Run sleep tests using float values.
* Update docs.
* Add HealthTest create method to fix db insertions.
* Update docs.
* Merge branch 'master' into isolate_tests
* Move settings to tests.test_settings.
* Move tests into tests directory.
* Treat tests/ as an application and define models and views for contextual usage.
* Update docs.
* Change HealthTest children to match examples in docs.
* Update docs.
* Update documentation.
* Remove method_decorator.
* Exception handle 'View' import.
* Remove migrations.
* Remove migrations.
* Isolate 'use case' in test suite.
* Remove dispatcher and scoring logic and implement in parent classes.
* Move 'health' tests.
* Clean up imports.
* Isolate scoring_helper for removal.
* Return http status_code for API get success and failure.
* Return http status_code for API get success and failure.
* Change test_name to test.
* Refactor
* Update 'update' field only on score change.
* Refactor into utils.
* Rename utils to scoring_helper
* Move change_date from a model attribute into severity JSON.
* Refactor for class-based views.
* Add method to delete test state from Health.
* Add method to delete asset.
* Update docs for class-based views.
* Allow UIDs to contain chars.
* Change to class-based views.
* Refactor
* Remove tests from matrix due to find_spec not being supported.
* Revert "Remove coverage from Travis config in favor of GitHub integration."
* Remove coverage from Travis config in favor of GitHub integration.
* Point badges to Gracenote account.
* Change to Gracenote GitHub account.
* Add Apache 2.0 headers
* Update to Apache 2.0
* Fix location of wsgi.py.

0.1.6 (2017-02-15)
++++++++++++++++++

* Publish 0.1.6
* Make changes for codecov.
* Change test config to use generic test names.
* Modify tests to use generic configuration.
* Change helper function to take multiple arguments.
* Modify UID to be passed as number.
* Change references from 'subscriber' to 'group'.
* Remove unused tests.
* Remove unneeded fixture.
* Change 'subscriber' key to a more general term 'group'.
* Remove unnecessary helper functions and unused dispatcher parameters.
* Pass ImportError directly.

0.1.5 (2017-01-25)
++++++++++++++++++

* Publish 0.1.5.
* Remove all packages from requirements files except jsonfield.

0.1.4 (2017-01-24)
++++++++++++++++++

* Push package changes for separating out configuration from application.
* Move config out of health_monitor application and into tests.
* Add HEALTH_MONITOR_CONFIG to settings.py to create a dynamic directory for configuration imports.
* Remove explicit unicode blank.
* Exclude flake8 testing for now.
* Try .travis.yml provided at https://github.com/pennersr/django-allauth/blob/master/.travis.yml.
* Try .travis.yml provided at https://github.com/pennersr/django-allauth/blob/master/.travis.yml.
* Modify tests and function for Python3.4 compatibility.
* Remove test coverage for now.
* Change to coverage3 for Travis CI tests.
* Use a simpler manage.py script.
* Update pip requirements and add django-jsonfield to install_requires.
* Change coverage version to '<4'
* Explicitly install coverage.
* Remove deprecated iteritems() call.
* Change travis script options.
* Change travis test script options.
* Add codecov.io badge.
* Remove deprecated iteritems() call.
* Configure Travis CI.
* Update dev pip requirements.
* Add unit, integration, and url tests.
* Update docs.
* Update docs.
* Reformat docs.
* Reformat docs.
* Update docs.
* Update docs.
* Change docs to reflect included migration.

0.1.3 (2017-01-23)
++++++++++++++++++

* Push new build with included migration for Health model.
* Add migration for Health model.
* Add preliminary documentation.
* Add some preliminary documentation.
* Add some preliminary documentation.
* Fix documentation markup.
* Fix documentation markup.

0.1.2 (2017-01-23)
++++++++++++++++++

* Update version.
* Use find_packages to add packages to setup.py.
* Update docs with project overview and import instructions.
* Update initial entries for documentation.
* Change project name from 'Health Monitor' to 'Django Health Manager'.
* Change setup.py package reference back to health_monitor.
* Change package name from health_monitor to django-health-monitor.

0.1.1 (2017-01-23)
++++++++++++++++++

* Add jsonfield to list of requirements.
* Copy existing test fixtures and configuration files (will need to be made generic later) for dispatcher mappings and scoring logic.
* Copy logic from functioning health application into health_monitor and rework code to function as a standalone app.
* Update requirements.txt files with current pip packages.
* Fix linter warning.
* Add manage.py and settings.py for initial app setup.
* Add env3 ti .gitignore.

0.1.0 (2016-11-04)
++++++++++++++++++

* First release on PyPI.
