from fixtures import *  # noqa: F401,F403
import unittest

# Import helper functions and test from CLN
from lightning.tests.test_splicing_insane import (
    make_pending_splice,
    wait_for_confirm,
    confirm,
    confirm_and_wait,
    confirm_funding_not_spent,
    wait_for_restart,
    test_splice_insane as _test_splice_insane,
)

# VLS does not support experimental-splicing
test_splice_insane = unittest.skip("VLS does not support experimental-splicing")(_test_splice_insane)
