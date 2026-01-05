from fixtures import *  # noqa: F401,F403
import unittest

# Import tests from CLN and wrap with VLS skip
from lightning.tests.test_splicing_disconnect import (
    test_splice_disconnect_sig as _test_splice_disconnect_sig,
    test_splice_disconnect_commit as _test_splice_disconnect_commit,
)

# VLS does not support experimental-splicing
test_splice_disconnect_sig = unittest.skip("VLS does not support experimental-splicing")(_test_splice_disconnect_sig)
test_splice_disconnect_commit = unittest.skip("VLS does not support experimental-splicing")(_test_splice_disconnect_commit)
