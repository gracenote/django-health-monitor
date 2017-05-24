- /health_test/
    - GET a list of all health tests
- /health_tests/<test>/?uids=<uids>&start_time=<start_time>&end_time=<end_time>
    - GET test results of a particular test with filters
- /health_test/<test>/<uid>/?start_time=<start_time>&end_time=<end_time>&latest=<latest>
    - GET test results of a particular test and uid with filters
- /health_test/<test>/<uid>/
    - POST test results of a particular test and uid

Where:

- <uid> is a unique identifier of an asset.
- <test> is the name of a health test.

And query string arguments:

- <uids> is a comma-separated list of uids (optional).
- <start_time> is a datetime string in ISO 8601 format (optional).
- <end_time> is a datetime string in  ISO 8601 format (optional).
- <latest> is a boolean value that if set to 1 or true will return the latest result in combination with start_time and end_time if provided.
- example: /health_test/heart/?uids=1,2,3&start_time=xxx&end_time=xxx
