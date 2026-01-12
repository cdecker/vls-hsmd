#!/usr/bin/env bash
set -e

# Compiler script for lightning submodule
# Automatically detects whether to use poetry or uv based on presence of poetry.lock

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIGHTNING_DIR="${SCRIPT_DIR}/../lightning"

cd "${LIGHTNING_DIR}"

if [ -f "poetry.lock" ]; then
    echo "Found poetry.lock, using poetry..."
    if ! command -v poetry &> /dev/null; then
        echo "Error: poetry.lock exists but poetry is not installed"
        exit 1
    fi
    
    # Install dependencies if needed (use Python 3.10 for compatibility)
    PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 poetry install
    
    # Run the command with poetry
    poetry run "$@"
else
    echo "No poetry.lock found, using uv..."
    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed"
        exit 1
    fi
    
    # Sync dependencies
    uv sync
    
    # Run the command with uv
    uv run "$@"
fi
