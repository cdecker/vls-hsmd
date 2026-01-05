from fixtures import *  # noqa: F401,F403
import unittest

# Import tests from CLN and wrap with VLS skip
from lightning.tests.test_splice import (
    test_script_splice_out as _test_script_splice_out,
    test_script_splice_in as _test_script_splice_in,
)

# VLS does not support experimental-splicing
test_script_splice_out = unittest.skip("VLS does not support experimental-splicing")(_test_script_splice_out)
test_script_splice_in = unittest.skip("VLS does not support experimental-splicing")(_test_script_splice_in)
