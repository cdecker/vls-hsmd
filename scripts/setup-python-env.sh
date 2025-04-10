#!/bin/bash
set -e
echo "Running in $(pwd)"

export PATH="$HOME/.local/bin:$PATH"

sudo apt-get update
sudo apt-get install -y curl

curl -LsSf https://astral.sh/uv/install.sh | sh

uv venv --python 3.12
uv tool install poetry
source .venv/bin/activate
uv pip install poetry-plugin-export
# refresh shell cache so that poetry and its plugin are visible
hash -r
uv pip install --no-deps -r <(POETRY_WARNINGS_EXPORT=false poetry export --without-hashes --with dev -f requirements.txt)
