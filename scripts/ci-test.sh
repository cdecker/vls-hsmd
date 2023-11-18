#!/bin/bash
set -e
echo "Running in $(pwd)"

basedir="$(pwd)/.."
ls -l "$basedir/bin"

export TIMEOUT=300
export DEVELOPER=${DEVELOPER:-1}
export PATH="$PATH:~/.local/bin:$basedir/bin"
export SLOW_MACHINE=1
export LIGHTNINGD_POSTGRES_NO_VACUUM=1
export TEST_CHECK_DBSTMTS=${TEST_CHECK_DBSTMTS:-0}
export COMPAT=${COMPAT:-1}
export TEST_DB_PROVIDER=${TEST_DB_PROVIDER:-"sqlite3"}
export TEST_NETWORK=${NETWORK:-"regtest"}
export PYTEST_SENTRY_ALWAYS_REPORT=1
export VALGRIND=0
export FUZZING=0
export RUST_BACKTRACE=1

poetry config virtualenvs.create false --local
poetry install

cat << EOF > pytest.ini
[pytest]
addopts=-p no:logging --color=yes --timeout=300 --timeout-method=signal --test-group-random-seed=42
markers =
    slow_test: marks tests as slow (deselect with '-m "not slow_test"')
EOF


GREENLIGHT_VERSION=$(./lightningd/lightningd --version)
export GREENLIGHT_VERSION

# This is run from vls-hsmd/lightning
# note that accessing this via a symlink doesn't work on gitlab CI runners - perhaps a docker bug
REMOTE_SIGNER_ALLOWLIST="$(pwd)/../remote_hsmd/TESTING_ALLOWLIST"
export REMOTE_SIGNER_ALLOWLIST

# All of the TEST_DIR manipulation is necessary to keep the total path
# length of the lightningd-rpc AF_UNIX socket shorter than 108

# TEST_DIR is set in .gitlab-ci.yml, make it a symlink to something in the project dir
rm -rf ${CI_PROJECT_DIR}/TESTS
mkdir -p ${CI_PROJECT_DIR}/TESTS
ln -sf ${CI_PROJECT_DIR}/TESTS ${TEST_DIR}

export RUST_LOG=debug


export PYTHONPATH=${PYTHONPATH}${PYTHONPATH:+:}contrib/pyln-client:contrib/pyln-testing:contrib/pyln-proto/:external/lnprototest:contrib/pyln-spec/bolt1:contrib/pyln-spec/bolt2:contrib/pyln-spec/bolt4:contrib/pyln-spec/bolt7 TEST_DEBUG=1 DEVELOPER=1 VALGRIND=0 && \
    printenv >  $TEST_DIR/ENV.log && \
    eatmydata python3 -m pytest tests/ -v -p no:logging --maxfail=5 --suppress-no-test-exit-code  -n=10 --show-capture=no 2>&1 | tee $TEST_DIR/ALL.log

# Capture the exit status of pytest
PYTEST_EXIT_CODE=${PIPESTATUS[0]}

# Prune useless directories
../scripts/prune-test-dir $TEST_DIR

# Use the captured exit code as the exit status of the script
exit $PYTEST_EXIT_CODE
