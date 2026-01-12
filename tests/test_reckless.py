from fixtures import *  # noqa: F401,F403
import unittest

# Import all tests and fixtures from CLN - tests are identical
from lightning.tests.test_reckless import (
    canned_github_server,
    test_basic_help,
    test_contextual_help,
    test_sources,
    test_search,
    test_install as _test_install,
    test_poetry_install as _test_poetry_install,
    test_local_dir_install as _test_local_dir_install,
    test_disable_enable as _test_disable_enable,
    test_tag_install as _test_tag_install,
)

# Skip tests that are broken in the current environment (native and vls)
# Issue: subprocess.CalledProcessError: Command '[.../bin/python3.12', '-m', 'ensurepip', ...]' returned non-zero exit status 127.
reason = "Broken in test env: ensurepip/python3.12 issue"
test_install = unittest.skip(reason)(_test_install)
test_poetry_install = unittest.skip(reason)(_test_poetry_install)
test_local_dir_install = unittest.skip(reason)(_test_local_dir_install)
test_disable_enable = unittest.skip(reason)(_test_disable_enable)
test_tag_install = unittest.skip(reason)(_test_tag_install)
