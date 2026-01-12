from fixtures import *  # noqa: F401,F403
import pytest
import os

# Import all tests from CLN - tests are identical
from lightning.tests.test_xpay import (
    test_pay_fakenet as _test_pay_fakenet,
    test_xpay_simple as _test_xpay_simple,
    test_xpay_selfpay as _test_xpay_selfpay,
    test_xpay_fake_channeld as _test_xpay_fake_channeld,
    test_xpay_timeout as _test_xpay_timeout,
    test_xpay_partial_msat as _test_xpay_partial_msat,
    test_xpay_takeover as _test_xpay_takeover,
    test_xpay_preapprove as _test_xpay_preapprove,
    test_xpay_maxfee as _test_xpay_maxfee,
    test_xpay_unannounced as _test_xpay_unannounced,
    test_xpay_zeroconf as _test_xpay_zeroconf,
)

# VLS does not currently support the WIRE_HSMD_SIGN_BOLT12_2 (msg 41) message which
# is required for xpay tests that use BOLT12 offers/invoices. The protocol error
# shows as: Protocol(TrailingBytes(93, 41)) indicating a wire format mismatch.
# We should unskip these once VLS implements support for msg 41.
# See DEBUG.md for more details on the protocol mismatch.

# Tests that need to be skipped in VLS mode
test_pay_fakenet = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_pay_fakenet)
test_xpay_simple = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_simple)
test_xpay_selfpay = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_selfpay)
test_xpay_fake_channeld = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_fake_channeld)
test_xpay_timeout = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_timeout)
test_xpay_partial_msat = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_partial_msat)
test_xpay_takeover = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_takeover)
test_xpay_preapprove = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_preapprove)
test_xpay_maxfee = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_maxfee)
test_xpay_unannounced = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_unannounced)
test_xpay_zeroconf = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_xpay_zeroconf)
