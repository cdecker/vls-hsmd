#!/bin/bash
# Patch all pyproject.toml files in lightning/contrib to add [project] tables
# This is needed for uv to install these packages

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PATCH_SCRIPT="$SCRIPT_DIR/patch_pyproject.py"

echo "Patching pyproject.toml files in lightning/contrib..."

# Make the patch script executable
chmod +x "$PATCH_SCRIPT"

# Find all pyproject.toml files in contrib
find "$ROOT_DIR/lightning/contrib" -name "pyproject.toml" -type f | while read -r toml_file; do
    echo "Processing: $toml_file"
    
    # Check if [project] table already exists
    if grep -q "^\[project\]" "$toml_file"; then
        echo "  -> Already has [project] table, skipping"
    else
        # Check if file is writable
        if [ ! -w "$toml_file" ]; then
            echo "  -> Making file writable..."
            chmod u+w "$toml_file" 2>/dev/null || sudo chmod u+w "$toml_file" 2>/dev/null || {
                echo "  -> Cannot make file writable, skipping"
                continue
            }
        fi
        
        # Patch the file using uv run (script has inline dependencies)
        if "$PATCH_SCRIPT" "$toml_file"; then
            echo "  -> Successfully patched"
        else
            echo "  -> Failed to patch (this may be expected for some files)"
        fi
    fi
    echo ""
done

echo "Done patching pyproject.toml files"
