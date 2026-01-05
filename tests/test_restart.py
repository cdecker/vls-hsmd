from fixtures import *  # noqa: F401,F403
import unittest

# Import test from CLN and wrap with VLS skip
from lightning.tests.test_restart import (
    test_agressive_restart as _test_agressive_restart,
)

# VLS does not support experimental-splicing
test_agressive_restart = unittest.skip("VLS does not support experimental-splicing")(_test_agressive_restart)
