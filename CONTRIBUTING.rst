============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Give Feedback
~~~~~~~~~~~~~

How are you using this package? We would love to know. Email s@seanchon.com with any feedback, suggestions, etc.

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/gracenote/django-health-monitor/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Django Health Monitor could always use more documentation, whether as part of the
official Django Health Monitor docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/gracenote/django-health-monitor/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `django-health-monitor` for local development.

1. Fork the `django-health-monitor` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:gracenote/django-health-monitor.git

3. Install your local copy into a virtualenv. Assuming you have virtualenv installed, this is how you set up your fork for local development::

    $ cd django-health-monitor/
    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements_dev.txt

4. Migrate "tests" application. (Note: A test implementation of this package runs in the tests directory.)::

    (venv)$ python manage.py makemigrations tests
    (venv)$ python manage.py migrate

5. Run the application locally::

    (venv)$ python manage.py runserver

   Check the endpoints in the browser after running

6. Create a branch for local development::

    (venv)$ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

7. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions with tox::

        (venv)$ flake8 health_monitor tests
        (venv)$ python manage.py test
        (venv)$ tox

   To get flake8 and tox, just pip install them into your virtualenv.

8. Commit your changes and push your branch to GitHub::

    (venv)$ git add .
    (venv)$ git commit -m "Your detailed description of your changes."
    (venv)$ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests. This project was inspired by `Readme-Driven
   Development <https://www.kennethreitz.org/essays/how-i-develop-things-and-why>`_.
   The current tests were written around the `API Reference
   <https://django-health-monitor.readthedocs.io/en/latest/api_reference.html>`_.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, and 3.3, and for PyPy. Check
   https://travis-ci.org/gracenote/django-health-monitor/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    (venv)$ python manage.py test tests.tests.test_integration_health
