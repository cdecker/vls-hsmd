#!/usr/bin/env bash
# Wrapper script for remote_hsmd_socket that strips --log-trace and --dev-debug-self
# These options are passed by CLN but not supported by VLS proxy

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Path to the actual remote_hsmd_socket binary
BINARY="$PROJECT_ROOT/target/debug/remote_hsmd_socket"

# Filter out unsupported arguments
FILTERED_ARGS=()
for arg in "$@"; do
    case "$arg" in
        --log-trace|--dev-debug-self)
            # Skip these arguments
            ;;
        *)
            # Keep all other arguments
            FILTERED_ARGS+=("$arg")
            ;;
    esac
done

# Execute the actual binary with filtered arguments
exec "$BINARY" "${FILTERED_ARGS[@]}"
