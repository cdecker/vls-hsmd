from fixtures import *  # noqa: F401,F403
import unittest

# Import all tests from CLN
from lightning.tests.test_askrene import (
    test_reserve,
    test_layers,
    test_layer_persistence,
    test_getroutes,
    test_getroutes_fee_fallback,
    test_getroutes_auto_sourcefree,
    test_getroutes_auto_localchans,
    test_fees_dont_exceed_constraints,
    test_sourcefree_on_mods,
    test_live_spendable,
    test_limits_fake_gossmap,
    test_max_htlc,
    test_min_htlc,
    test_min_htlc_after_excess,
    test_real_data,
    test_real_biases,
    test_askrene_fake_channeld as _test_askrene_fake_channeld,
)

test_askrene_fake_channeld = unittest.skip("STATUS_FAIL_MASTER_IO and DatabaseAlreadyOpen")(_test_askrene_fake_channeld)