from fixtures import *  # noqa: F401,F403

# Import all tests from CLN - tests are identical
from lightning.tests.test_xpay import (
    test_pay_fakenet,
    test_xpay_simple,
    test_xpay_selfpay,
    test_xpay_fake_channeld,
    test_xpay_timeout,
    test_xpay_partial_msat,
    test_xpay_takeover,
    test_xpay_preapprove,
    test_xpay_maxfee,
    test_xpay_unannounced,
    test_xpay_zeroconf,
)
