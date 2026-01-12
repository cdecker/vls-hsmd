from fixtures import *  # noqa: F401,F403
import pytest
import os

# Import test from CLN
from lightning.tests.test_restart import (
    test_agressive_restart as _test_agressive_restart,
)

# VLS does not support experimental-splicing
test_agressive_restart = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support experimental-splicing")(_test_agressive_restart)