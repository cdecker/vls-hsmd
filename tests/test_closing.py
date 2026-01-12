import os
import pytest
from fixtures import *  # noqa: F401,F403

# Import all tests from CLN
from lightning.tests.test_closing import (
    test_closing_simple,
    test_closing_while_disconnected,
    test_closing_disconnected_notify,
    test_closing_id,
    test_closing_different_fees,
    test_closing_negotiation_reconnect as _test_closing_negotiation_reconnect,
    test_closing_specified_destination,
    test_closing_negotiation_step_30pct,
    test_closing_negotiation_step_100pct,
    test_closing_negotiation_step_1sat,
    test_closing_negotiation_step_700sat,
    test_penalty_inhtlc,
    test_penalty_outhtlc,
    test_channel_lease_falls_behind,
    test_channel_lease_post_expiry,
    test_channel_lease_unilat_closes,
    test_channel_lease_lessor_cheat,
    test_channel_lease_lessee_cheat,
    test_penalty_htlc_tx_fulfill as _test_penalty_htlc_tx_fulfill,
    test_penalty_htlc_tx_timeout as _test_penalty_htlc_tx_timeout,
    test_penalty_rbf_normal,
    test_onchain_first_commit,
    test_onchain_unwatch,
    test_onchaind_replay,
    test_onchain_dust_out,
    test_onchain_timeout,
    test_onchain_middleman_simple,
    test_onchain_middleman_their_unilateral_in,
    test_onchain_their_unilateral_out,
    test_listfunds_after_their_unilateral,
    test_onchain_feechange,
    test_onchain_all_dust,
    test_onchain_different_fees,
    test_permfail_new_commit,
    test_onchain_multihtlc_our_unilateral,
    test_onchain_multihtlc_their_unilateral,
    test_permfail_htlc_in,
    test_permfail_htlc_out,
    test_permfail,
    test_shutdown,
    test_option_upfront_shutdown_script,
    test_invalid_upfront_shutdown_script,
    test_segwit_shutdown_script,
    test_closing_higherfee,
    test_htlc_rexmit_while_closing,
    test_you_forgot_closed_channel,
    test_you_forgot_closed_channel_onchain,
    test_segwit_anyshutdown,
    test_anysegwit_close_needs_feature,
    test_close_feerate_range,
    test_close_twice,
    test_close_weight_estimate,
    test_onchain_close_upstream,
    test_onchain_rexmit_tx,
    test_closing_anchorspend_htlc_tx_rbf,
    test_htlc_no_force_close,
    test_closing_tx_valid,
    test_closing_minfee,
    test_peer_anchor_push,
    test_closing_cpfp,
    test_closing_no_anysegwit_retry,
    test_closing_ignore_fee_limits,
    test_anchorspend_using_to_remote,
    test_onchain_reestablish_reply,
    test_onchain_slow_anchor,
)

# test_closing_negotiation_reconnect times out (>180s) in both native and VLS modes.
# This appears to be a broken test in the CLN test suite itself.
test_closing_negotiation_reconnect = pytest.mark.skip(
    reason="Test times out in both native and VLS modes (broken CLN test)"
)(_test_closing_negotiation_reconnect)

# Penalty HTLC tests time out with VLS. These tests involve force-closing channels
# and claiming HTLCs via penalty transactions when the peer cheats. VLS appears to
# hang when processing these penalty transaction scenarios.
test_penalty_htlc_tx_fulfill = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out when processing penalty transactions for HTLC fulfillment"
)(_test_penalty_htlc_tx_fulfill)

test_penalty_htlc_tx_timeout = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out when processing penalty transactions for HTLC timeout"
)(_test_penalty_htlc_tx_timeout)
