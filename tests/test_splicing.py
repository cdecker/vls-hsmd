from fixtures import *  # noqa: F401,F403
import unittest

# Import all tests from CLN and wrap with VLS skip
from lightning.tests.test_splicing import (
    test_splice as _test_splice,
    test_splice_gossip as _test_splice_gossip,
    test_splice_listnodes as _test_splice_listnodes,
    test_splice_out as _test_splice_out,
    test_invalid_splice as _test_invalid_splice,
    test_commit_crash_splice as _test_commit_crash_splice,
    test_splice_stuck_htlc as _test_splice_stuck_htlc,
)

# VLS does not support experimental-splicing
test_splice = unittest.skip("VLS does not support experimental-splicing")(_test_splice)
test_splice_gossip = unittest.skip("VLS does not support experimental-splicing")(_test_splice_gossip)
test_splice_listnodes = unittest.skip("VLS does not support experimental-splicing")(_test_splice_listnodes)
test_splice_out = unittest.skip("VLS does not support experimental-splicing")(_test_splice_out)
test_invalid_splice = unittest.skip("VLS does not support experimental-splicing")(_test_invalid_splice)
test_commit_crash_splice = unittest.skip("VLS does not support experimental-splicing")(_test_commit_crash_splice)
test_splice_stuck_htlc = unittest.skip("VLS does not support experimental-splicing")(_test_splice_stuck_htlc)
