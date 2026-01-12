#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "tomli",
#     "tomli_w",
# ]
# ///
"""
Patch a pyproject.toml file to add [project] table from legacy Poetry config.

This script converts legacy Poetry-style pyproject.toml files to the modern
PEP 621 format that uv requires by extracting information from [tool.poetry]
and creating a [project] table.

Usage:
    ./patch_pyproject.py <path_to_pyproject.toml>
    uv run scripts/patch_pyproject.py <path_to_pyproject.toml>
"""

import sys
import argparse
from pathlib import Path
import tomli
import tomli_w


def convert_poetry_dependency(dep_spec):
    """
    Convert Poetry dependency specification to PEP 621 format.
    
    Poetry format examples:
    - "^1.0.0" -> ">=1.0.0,<2.0.0"
    - "~1.2.3" -> ">=1.2.3,<1.3.0"
    - ">=1.0.0" -> ">=1.0.0"
    - "*" -> ""
    - {"version": "^1.0", "optional": true} -> ">=1.0,<2.0"
    """
    if isinstance(dep_spec, dict):
        version = dep_spec.get("version", "*")
        dep_spec = version
    
    if dep_spec == "*":
        return ""
    
    # Handle caret (^) requirements
    if dep_spec.startswith("^"):
        version = dep_spec[1:]
        parts = version.split(".")
        if len(parts) >= 1:
            major = int(parts[0])
            next_major = major + 1
            return f">={version},<{next_major}.0.0"
    
    # Handle tilde (~) requirements
    if dep_spec.startswith("~"):
        version = dep_spec[1:]
        parts = version.split(".")
        if len(parts) >= 2:
            major, minor = parts[0], parts[1]
            next_minor = int(minor) + 1
            return f">={version},<{major}.{next_minor}.0"
    
    # Already in PEP 440 format
    return dep_spec


def extract_project_info(toml_data):
    """Extract project information from tool.poetry section."""
    poetry = toml_data.get("tool", {}).get("poetry", {})
    
    if not poetry:
        raise ValueError("No [tool.poetry] section found in pyproject.toml")
    
    # Build the project table
    project = {
        "name": poetry.get("name"),
        "version": poetry.get("version", "0.0.0"),
        "description": poetry.get("description", ""),
    }
    
    # Add authors if present
    authors_list = poetry.get("authors", [])
    if authors_list:
        # Convert "Name <email>" to {"name": "Name", "email": "email"}
        authors = []
        for author in authors_list:
            if "<" in author and ">" in author:
                name, email = author.split("<")
                email = email.rstrip(">").strip()
                name = name.strip()
                authors.append({"name": name, "email": email})
            else:
                authors.append({"name": author.strip()})
        project["authors"] = authors
    
    # Add license
    license_info = poetry.get("license")
    if license_info:
        project["license"] = {"text": license_info}
    
    # Add readme
    readme = poetry.get("readme")
    if readme:
        project["readme"] = readme
    
    # Add homepage/repository as URLs
    urls = {}
    if poetry.get("homepage"):
        urls["Homepage"] = poetry["homepage"]
    if poetry.get("repository"):
        urls["Repository"] = poetry["repository"]
    if urls:
        project["urls"] = urls
    
    # Add classifiers
    classifiers = poetry.get("classifiers", [])
    if classifiers:
        project["classifiers"] = classifiers
    
    # Add requires-python
    python_version = poetry.get("dependencies", {}).get("python")
    if python_version and python_version != "*":
        project["requires-python"] = convert_poetry_dependency(python_version)
    
    # Add dependencies
    dependencies = []
    poetry_deps = poetry.get("dependencies", {})
    for dep_name, dep_spec in poetry_deps.items():
        if dep_name == "python":
            continue
        
        version_spec = convert_poetry_dependency(dep_spec)
        if version_spec:
            dependencies.append(f"{dep_name}{version_spec}")
        else:
            dependencies.append(dep_name)
    
    if dependencies:
        project["dependencies"] = dependencies
    
    # Add optional dependencies (extras)
    extras = poetry.get("extras", {})
    if extras:
        optional_deps = {}
        for extra_name, extra_deps in extras.items():
            optional_deps[extra_name] = extra_deps
        project["optional-dependencies"] = optional_deps
    
    return project


def patch_pyproject(file_path):
    """Patch a pyproject.toml file with [project] table."""
    import os
    import stat
    
    path = Path(file_path)
    
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    # Make file writable if it's not
    current_mode = path.stat().st_mode
    if not (current_mode & stat.S_IWUSR):
        os.chmod(path, current_mode | stat.S_IWUSR)
    
    # Read the existing file
    with open(path, "rb") as f:
        toml_data = tomli.load(f)
    
    # Check if [project] already exists
    if "project" in toml_data:
        print(f"Warning: [project] table already exists in {file_path}")
        print("Skipping to avoid overwriting existing configuration.")
        return True
    
    try:
        # Extract project info from tool.poetry
        project_info = extract_project_info(toml_data)
        
        # Add [project] table at the beginning
        new_toml = {"project": project_info}
        
        # Add all other tables
        for key, value in toml_data.items():
            if key != "project":
                new_toml[key] = value
        
        # Create backup
        backup_path = path.with_suffix(".toml.bak")
        with open(backup_path, "wb") as f:
            tomli_w.dump(toml_data, f)
        print(f"Created backup: {backup_path}")
        
        # Write patched file
        with open(path, "wb") as f:
            tomli_w.dump(new_toml, f)
        
        print(f"Successfully patched {file_path}")
        print(f"Added [project] table with:")
        print(f"  - name: {project_info.get('name')}")
        print(f"  - version: {project_info.get('version')}")
        print(f"  - {len(project_info.get('dependencies', []))} dependencies")
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Patch pyproject.toml to add [project] table from Poetry config"
    )
    parser.add_argument(
        "file_path",
        help="Path to the pyproject.toml file to patch"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without modifying files"
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        path = Path(args.file_path)
        if not path.exists():
            print(f"Error: File not found: {args.file_path}")
            return 1
        
        with open(path, "rb") as f:
            toml_data = tomli.load(f)
        
        try:
            project_info = extract_project_info(toml_data)
            print("Would create [project] table with:")
            print(tomli_w.dumps({"project": project_info}))
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    success = patch_pyproject(args.file_path)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
