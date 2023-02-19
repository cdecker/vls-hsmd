#!/bin/bash
set -e
echo "Running in $(pwd)"

export ARCH=${ARCH:-64}
export BOLTDIR=bolts
export CC=${COMPILER:-gcc}
export COMPAT=${COMPAT:-1}
export DEVELOPER=${DEVELOPER:-1}
export EXPERIMENTAL_FEATURES=${EXPERIMENTAL_FEATURES:-0}
export PATH="$CWD/dependencies/bin:$HOME/.local/bin:$PATH"
export LIGHTNINGD_POSTGRES_NO_VACUUM=1

# problem in gitlab CI runners with symlinks?!
# assume we are running inside the CLN directory
REMOTE_SIGNER_ALLOWLIST="$(pwd)/../remote_hsmd/TESTING_ALLOWLIST"
export REMOTE_SIGNER_ALLOWLIST


pip3 install --user poetry
poetry config virtualenvs.create false --local
poetry install

git clone https://github.com/lightning/bolts.git ../${BOLTDIR}
git submodule update --init --recursive

./configure CC="$CC"
cat config.vars

touch doc/index.rst

eatmydata make -j32
