from fixtures import *  # noqa: F401,F403

# Import all tests and fixtures from CLN - tests are identical
from lightning.tests.test_reckless import (
    canned_github_server,
    test_basic_help,
    test_contextual_help,
    test_sources,
    test_search,
    test_install,
    test_poetry_install,
    test_local_dir_install,
    test_disable_enable,
    test_tag_install,
)
