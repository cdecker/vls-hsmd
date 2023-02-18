#!/bin/bash
set -e
echo "Running in $(pwd)"

export TIMEOUT=900
export SLOW_MACHINE=1
export DEVELOPER=${DEVELOPER:-1}
export EXPERIMENTAL_FEATURES=${EXPERIMENTAL_FEATURES:-0}
export TEST_CHECK_DBSTMTS=${TEST_CHECK_DBSTMTS:-0}
export TEST_DB_PROVIDER=${TEST_DB_PROVIDER:-"sqlite3"}
export TEST_NETWORK=${NETWORK:-"regtest"}
export PYTEST_SENTRY_ALWAYS_REPORT=1
export COMPAT=${COMPAT:-1}
export VALGRIND=0
export FUZZING=0

cat << EOF > pytest.ini
[pytest]
addopts=-p no:logging --color=yes --timeout=1800 --timeout-method=thread --test-group-random-seed=42
markers =
    slow_test: marks tests as slow (deselect with '-m "not slow_test"')
EOF


GREENLIGHT_VERSION=$(./lightningd/lightningd --version)
export GREENLIGHT_VERSION

PYTHONPATH=${PYTHONPATH}${PYTHONPATH:+:}contrib/pyln-client:contrib/pyln-testing:contrib/pyln-proto/:external/lnprototest:contrib/pyln-spec/bolt1:contrib/pyln-spec/bolt2:contrib/pyln-spec/bolt4:contrib/pyln-spec/bolt7 TEST_DEBUG=1 DEVELOPER=1 VALGRIND=0 \
  eatmydata python3 -m pytest tests/ -v -p no:logging --maxfail=5 --suppress-no-test-exit-code  -n=10
