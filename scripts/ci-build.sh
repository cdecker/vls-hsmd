#!/bin/bash
set -e
echo "Running in $(pwd)"

export ARCH=${ARCH:-64}
export BOLTDIR=bolts
export CC=${COMPILER:-gcc}
export COMPAT=${COMPAT:-1}
export DEVELOPER=${DEVELOPER:-1}
export PATH="$CWD/dependencies/bin:$HOME/.local/bin:$PATH"
export LIGHTNINGD_POSTGRES_NO_VACUUM=1

git clone https://github.com/lightning/bolts.git ../${BOLTDIR}
git submodule update --init --recursive

./configure CC="$CC"
cat config.vars

touch doc/index.rst

eatmydata make -j32
