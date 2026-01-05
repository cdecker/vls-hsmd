from fixtures import *  # noqa: F401,F403
import os
import unittest

# Import all tests and helper functions from CLN
from lightning.tests.test_opening import (
    find_next_feerate,
    test_queryrates as _test_queryrates,
    test_multifunding_v2_best_effort,
    test_v2_open_sigs_reconnect_2,
    test_v2_open_sigs_reconnect_1 as _test_v2_open_sigs_reconnect_1,
    test_v2_open_sigs_out_of_order,
    test_v2_fail_second,
    test_v2_open_sigs_restart_while_dead,
    test_v2_rbf_single as _test_v2_rbf_single,
    test_v2_rbf_abort_retry as _test_v2_rbf_abort_retry,
    test_v2_rbf_abort_channel_opens as _test_v2_rbf_abort_channel_opens,
    test_v2_rbf_liquidity_ad as _test_v2_rbf_liquidity_ad,
    test_v2_rbf_multi as _test_v2_rbf_multi,
    test_rbf_reconnect_init,
    test_rbf_reconnect_ack,
    test_rbf_reconnect_tx_construct as _test_rbf_reconnect_tx_construct,
    test_rbf_reconnect_tx_sigs as _test_rbf_reconnect_tx_sigs,
    test_rbf_to_chain_before_commit as _test_rbf_to_chain_before_commit,
    test_rbf_no_overlap as _test_rbf_no_overlap,
    test_rbf_fails_to_broadcast as _test_rbf_fails_to_broadcast,
    test_rbf_broadcast_close_inflights as _test_rbf_broadcast_close_inflights,
    test_rbf_non_last_mined as _test_rbf_non_last_mined,
    test_funder_options as _test_funder_options,
    test_funder_contribution_limits as _test_funder_contribution_limits,
    test_inflight_dbload as _test_inflight_dbload,
    test_zeroconf_mindepth,
    test_zeroconf_open as _test_zeroconf_open,
    test_zeroconf_public as _test_zeroconf_public,
    test_zeroconf_forward as _test_zeroconf_forward,
    test_buy_liquidity_ad_no_v2,
    test_v2_replay_bookkeeping as _test_v2_replay_bookkeeping,
    test_buy_liquidity_ad_check_bookkeeping as _test_buy_liquidity_ad_check_bookkeeping,
    test_scid_alias_private,
    test_zeroconf_multichan_forward as _test_zeroconf_multichan_forward,
    test_zeroreserve,
    test_zeroreserve_mixed,
    test_zeroreserve_alldust,
    test_coinbase_unspendable,
    test_openchannel_no_confirmed_inputs_opener,
    test_openchannel_no_unconfirmed_inputs_accepter as _test_openchannel_no_unconfirmed_inputs_accepter,
    test_no_anchor_liquidity_ads,
    test_commitment_feerate,
    test_anchor_min_emergency,
    test_fundchannel_utxo_too_small,
    test_opening_explicit_channel_type,
    test_multifunding_all_amount,
)

# Apply VLS-specific conditional skips
# These tests require features not yet implemented in VLS
test_queryrates = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native", "handle_sign_option_will_fund_offer unimplemented")(_test_queryrates)
test_v2_rbf_abort_retry = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native", "handle_sign_option_will_fund_offer unimplemented")(_test_v2_rbf_abort_retry)
test_v2_rbf_liquidity_ad = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native", "handle_sign_option_will_fund_offer unimplemented")(_test_v2_rbf_liquidity_ad)
test_funder_options = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native", "handle_sign_option_will_fund_offer unimplemented")(_test_funder_options)
test_funder_contribution_limits = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native", "handle_sign_option_will_fund_offer unimplemented")(_test_funder_contribution_limits)

# These tests require dual-funding/splicing support
test_v2_open_sigs_reconnect_1 = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_v2_open_sigs_reconnect_1)
test_v2_rbf_single = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_v2_rbf_single)
test_v2_rbf_abort_channel_opens = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_v2_rbf_abort_channel_opens)
test_v2_rbf_multi = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_v2_rbf_multi)
test_rbf_reconnect_tx_construct = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_reconnect_tx_construct)
test_rbf_reconnect_tx_sigs = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_reconnect_tx_sigs)
test_rbf_to_chain_before_commit = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_to_chain_before_commit)
test_rbf_no_overlap = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_no_overlap)
test_rbf_fails_to_broadcast = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_fails_to_broadcast)
test_rbf_broadcast_close_inflights = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_broadcast_close_inflights)
test_rbf_non_last_mined = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_rbf_non_last_mined)
test_inflight_dbload = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_inflight_dbload)
test_zeroconf_open = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_zeroconf_open)
test_zeroconf_public = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_zeroconf_public)
test_zeroconf_forward = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_zeroconf_forward)
test_v2_replay_bookkeeping = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_v2_replay_bookkeeping)
test_buy_liquidity_ad_check_bookkeeping = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_buy_liquidity_ad_check_bookkeeping)
test_zeroconf_multichan_forward = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_zeroconf_multichan_forward)
test_openchannel_no_unconfirmed_inputs_accepter = unittest.skipIf(os.getenv("VLS_MODE") != "cln:native" and os.getenv("VLS_SKIP_SPLICE_TESTS") == "1", "VLS dual-funding/splicing support")(_test_openchannel_no_unconfirmed_inputs_accepter)
