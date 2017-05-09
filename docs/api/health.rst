- /health/
    - GET a list of all health uids
- /health/<uid>/
    - GET the health of a particular uid
    - DELETE the health of a particular uid
- /health/<uid>/<group>/
    - GET the health of a particular uid and group
    - DELETE health of a particular uid and group
- /health/<uid>/<group>/<test>/
    - GET the health of a particular uid and group and test
    - DELETE the health of a particular uid and group and test

Where:

- <uid> is a unique identifier of an asset.
- <group> is the name of a group of tests.
- <test> is the name of a health test.
