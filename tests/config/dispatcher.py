"""All parameters associated with tests should go into the dispatcher dictionary.

dispatcher[test_name] = name of tests
dispatcher[test_name]['scoring_logic'] = name of scoring test in scoring_logic.py
dispatcher[test_name]['params'] = test result values to be passed to calculate score using scoring_logic.py
dispatcher[test_name]['group'] = list of groups which this test is revelant for

Example:
    dispatcher = {
        'heart': {
            'scoring_logic': 'heart',
            'params': {
                'heartrate': 'heartrate',
                'arrhythmia': 'arrhythmia',
            },
            'group': ['doctor', ],
        },
        'sleep': {
            'scoring_logic': 'sleep',
            'params': {
                'quality': 'quality',
            },
            'group': ['doctor', ],
            'start_time': 'start_time',
            'end_time': 'end_time',
        }
    }
"""


def get_dispatcher(original_dispatcher=False):
    dispatcher = {
        'heart': {
            'scoring_logic': 'heart',
            'params': {
                'heartrate': 'heartrate',
                'arrhythmia': 'arrhythmia',
            },
            'group': ['doctor', ],
        },
        'sleep': {
            'scoring_logic': 'sleep',
            'params': {
                'quality': 'quality',
            },
            'group': ['doctor', ],
            'start_time': 'start_time',
            'end_time': 'end_time',
        }
    }
    return dispatcher
