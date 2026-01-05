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

# WORKAROUND for https://github.com/ElementsProject/lightning/issues/6529
pip3 install --break-system-packages --ignore-installed blinker

# WORKAROUND
pip install --break-system-packages certifi==2023.7.22

find . -name "uv.lock" -print

# uv is already installed in most CI environments, but ensure it's available
pip3 install --break-system-packages --user uv || true
uv sync

git clone https://github.com/lightning/bolts.git ../${BOLTDIR}
git submodule update --init --recursive

./configure CC="$CC"
cat config.vars

touch doc/index.rst

eatmydata make -j32
