#!/usr/bin/env bash
set -xeuo pipefail

# Install from setup.py
pip install -e .
mkdir report
# Run WebSock in background
python scripts/autobahn-test.py &
# Start autobahn test
docker run -it -v $(pwd)/report:/autobahn-python-master/wstest/reports/servers --network="host" haegi/autobahn-testsuite make test_server