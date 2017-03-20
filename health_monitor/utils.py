"""
   Copyright 2017 Gracenote

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

"""Import user-defined configuration files declared in settings.py"""
import sys

from django.conf import settings
sys.path.append(settings.HEALTH_MONITOR_CONFIG)

try:
    from dispatcher import get_dispatcher
except ImportError as e:
    raise ImportError(e)

try:
    import scoring_logic
except ImportError as e:
    raise ImportError(e)

"""
Functions accessing scoring_logic.py
"""


def get_score(test_name, **kwargs):
    """Calculate a score red=4, orange=3, yellow=2, green=1 based off of the scoring logic."""
    # for integrity purposes, if method_name is not in dispatcher, raise Exception
    dispatcher = get_dispatcher()
    if test_name not in dispatcher.keys():
        raise LookupError("test for '{}' not implemented in scoring_logic.py".format(test_name))

    method_name = dispatcher[test_name]['scoring_logic']

    # get method based on method_name
    method = getattr(scoring_logic, method_name)

    # get params to pass to method
    # checks against dispatcher dictionary for integrity
    params = {}
    for key, value in kwargs.items():
        try:
            params[dispatcher[test_name]['params'][key]] = value
        except Exception:
            raise LookupError('param \'{}\' not implemented in test for \'{}\' in scoring_logic.py'.format(key, test_name))

    try:
        return method(**params)
    except Exception as e:
        raise LookupError(str(e))
        return 0


"""
Functions accessing dispatcher.py
"""


def calculate_severity(group, state):
    """Return the highest score in state dict."""
    test_scores = [1, ]
    for test in state[group].keys():
        if state[group][test]['score']:
            test_scores.append(state[group][test]['score'])

    return max(test_scores)


def get_health_keys(group):
    """Return an array of tests associated with each group."""
    dispatcher = get_dispatcher(original_dispatcher=True)
    health_keys = [x for x in dispatcher.keys() if group in dispatcher[x]['group']]

    return health_keys


def get_group_list_for_test(test_name):
    """Return a list of group for a given test."""
    dispatcher = get_dispatcher()
    return dispatcher[test_name]['group']