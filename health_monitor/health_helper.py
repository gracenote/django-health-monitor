from health_monitor.config.dispatcher import get_dispatcher
from health_monitor.config import scoring_logic


"""
Functions accessing health/config/scoring_logic.py
"""


def get_score(test_name, **kwargs):
    """Calculate a score red=4, orange=3, yellow=2, green=1 based off of the scoring logic."""
    # for integrity purposes, if method_name is not in dispatcher, raise Exception
    dispatcher = get_dispatcher()
    if test_name not in dispatcher.keys():
        raise LookupError("test for '{}' not implemented in scoring_logic.py".format(test_name))

    method_name = dispatcher[test_name]['method']

    # get method based on method_name
    method = getattr(scoring_logic, method_name)

    # get params to pass to method
    # checks against dispatcher dictionary for integrity
    params = {}
    for key, value in kwargs.iteritems():
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
Functions accessing health/config/dispatcher.py
"""


def get_legend(subscriber):
    """Return a tuple of tests and descriptions associated with each subscriber."""
    legend = {}
    dispatcher = get_dispatcher(original_dispatcher=True)
    health_keys = get_health_keys(subscriber)
    for key in health_keys:
        legend[key.decode('unicode-escape')] = dispatcher[key]['description'] if 'description' in dispatcher[key] else None

    return sorted(legend.items())


def calculate_severity(subscriber_state):
    """Return the highest score in state dict."""
    test_scores = [1, ]
    for test in subscriber_state.keys():
        test_scores.append(subscriber_state[test]['score'])

    return max(test_scores)


def get_health_keys(subscriber):
    """Return an array of tests associated with each subscriber."""
    dispatcher = get_dispatcher(original_dispatcher=True)
    health_keys = []
    for key in dispatcher.keys():
        if subscriber in dispatcher[key]['subscriber']:
            health_keys.append(key.decode('unicode-escape'))

    return health_keys


def get_subscribers_list_for_test(test_name):
    """Return a list of subscribers for a given test."""
    dispatcher = get_dispatcher()
    return dispatcher[test_name]['subscriber']


# def get_latest_health_state(tui):
#     """Return the latest health state for a given TUI."""
#     health_state = {}
#     for subscriber in Subscriber.objects.values_list():
#         health_state[subscriber[1].lower()] = {}
#     dispatcher = get_dispatcher(original_dispatcher=True)
#
#     for test in dispatcher.keys():
#         score = get_latest_score(tui, test)
#         for subscriber in dispatcher[test]['subscriber']:
#             health_state[subscriber][test] = score
#
#     return health_state


def get_test_list(subscriber=None):
    """Get entire list of tests or those associated with a subscriber."""
    test_list = []
    dispatcher = get_dispatcher(original_dispatcher=True)

    if not subscriber:
        return sorted(dispatcher.keys())
    else:
        for key, value in dispatcher.iteritems():
            if subscriber.lower() in value['subscriber']:
                test_list.append(key)

    return sorted(test_list)
