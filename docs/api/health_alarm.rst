- /health_alarm/
    - GET a list of all groups
- /health_alarm/<group>/
    - GET a list of all health tests for a particular group
- /health_alarm/<group>/<test>/?score=<score>&aggregate_percent=<aggregate_percent>&repetition=<repetition>&repetition_percent=<repetition_percent>
    - GET a health alarm for a particular test (calculate whether or not an alarm condition exists and return `uids` in failure state)

Where:

- <group> is the name of a group of tests.
- <test> is the name of a health test.

And query string arguments:

- <score> is the minimum `score` needed to trigger a failure.
- <aggregate_percent> is the minimum `percent` of total assets in a failure state needed to trigger an alarm (optional). This is by default 0.
- <repetition> is the minimum number of successive test results in a failure state needed to trigger an alarm (optional). This is by default 1.
- <repetition_percent> is the minimum percent within the prior defined repetition in a failure state needed to trigger an alarm (optional). This is by default 100.
