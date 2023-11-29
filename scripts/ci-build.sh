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
pip3 install --ignore-installed blinker

# WORKAROUND
pip install certifi==2023.7.22

find . -name "poetry.lock" -print

pip3 install --user poetry
poetry config virtualenvs.create false --local
poetry install

git clone https://github.com/lightning/bolts.git ../${BOLTDIR}
git submodule update --init --recursive

./configure CC="$CC"
cat config.vars

touch doc/index.rst

eatmydata make -j32
