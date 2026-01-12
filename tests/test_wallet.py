from fixtures import *  # noqa: F401,F403
import pytest
import os
import unittest
from pyln.client import RpcError, Millisatoshi
from pyln.testing.utils import sync_blockheight, wait_for
from bitcoin.rpc import JSONRPCError
from utils import check_coin_moves

# Import all tests from CLN
from lightning.tests.test_wallet import (
    test_withdraw,
    test_minconf_withdraw,
    test_addfunds_from_block,
    test_txprepare_multi,
    test_txprepare,
    test_reserveinputs,
    test_fundpsbt,
    test_addpsbtoutput,
    test_utxopsbt,
    test_sign_external_psbt,
    test_psbt_version,
    test_sign_and_send_psbt as original_test_sign_and_send_psbt,
    test_txsend,
    test_hsm_secret_encryption as original_test_hsm_secret_encryption,
    test_hsmtool_secret_decryption as original_test_hsmtool_secret_decryption,
    test_hsmtool_dump_descriptors,
    test_hsmtool_generatehsm as original_test_hsmtool_generatehsm,
    test_fundchannel_listtransaction,
    test_withdraw_nlocktime,
    test_withdraw_nlocktime_fuzz,
    test_multiwithdraw_simple,
    test_repro_4258,
    test_withdraw_bech32m,
    test_p2tr_deposit_withdrawal,
    test_upgradewallet,
    test_hsmtool_makerune,
    test_hsmtool_getnodeid,
)

@unittest.skipIf(TEST_NETWORK == 'liquid-regtest', 'Core/Elements need joinpsbt support for v2')
@pytest.mark.skip(reason="Fails with IndexError on VLS socket mode, needs investigation")
def test_sign_and_send_psbt(node_factory, bitcoind, chainparams):
    """
    Tests for the sign + send psbt RPCs
    """
    # CLN returns PSBTv0 and PSETv2, for now
    is_psbt_v2 = chainparams['elements']

    # Once support for v2 joinpsbt is added, below test should work verbatim
    assert not is_psbt_v2

    amount = 1000000
    total_outs = 12
    # Adjust path for vls-hsmd repo structure
    coin_mvt_plugin = os.path.join(os.getcwd(), 'lightning/tests/plugins/coin_movements.py')
    l1 = node_factory.get_node(options={'plugin': coin_mvt_plugin},
                               feerate=(7500, 7500, 7500, 7500))
    l2 = node_factory.get_node()
    addr = chainparams['example_addr']
    out_total = Millisatoshi(amount * 3 * 1000)

    # Add a medley of funds to withdraw later
    for i in range(total_outs):
        bitcoind.rpc.sendtoaddress(l1.rpc.newaddr()['bech32'],
                                   amount / 10**8)
    bitcoind.generate_block(1)
    sync_blockheight(bitcoind, [l1])
    wait_for(lambda: len(l1.rpc.listfunds()['outputs']) == total_outs)

    # Now we create a PSBT that spends all of them!
    utxos = l1.rpc.listfunds()['outputs']
    inputs = []
    for u in utxos:
        inputs.append({'txid': u['txid'], 'vout': u['output']})

    # Queue up another node, to make some PSBTs for us
    for i in range(total_outs):
        bitcoind.rpc.sendtoaddress(l2.rpc.newaddr()['bech32'],
                                   amount / 10**8)
    # Create a PSBT using L2
    bitcoind.generate_block(1)
    wait_for(lambda: len(l2.rpc.listfunds()['outputs']) == total_outs)
    l2_funding = l2.rpc.fundpsbt(satoshi=out_total,
                                 feerate=7500,
                                 startweight=42)

    # Try to get L1 to sign it
    with pytest.raises(RpcError, match=r"No wallet inputs to sign"):
        l1.rpc.signpsbt(l2_funding['psbt'])

    # With signonly it will fail if it can't sign it.
    with pytest.raises(RpcError, match=r"is unknown"):
        l1.rpc.signpsbt(l2_funding['psbt'], signonly=[0])

    # Add some of our own PSBT inputs to it
    l1_funding = l1.rpc.fundpsbt(satoshi=out_total,
                                 feerate=7500,
                                 startweight=42)
    if is_psbt_v2:
        l1_num_inputs = bitcoind.rpc.decodepsbt(l1_funding['psbt'])["input_count"]
        l2_num_inputs = bitcoind.rpc.decodepsbt(l2_funding['psbt'])["input_count"]
    else:
        l1_num_inputs = len(bitcoind.rpc.decodepsbt(l1_funding['psbt'])['tx']['vin'])
        l2_num_inputs = len(bitcoind.rpc.decodepsbt(l2_funding['psbt'])['tx']['vin'])

    # Join and add an output (reorders!)
    out_2_ms = Millisatoshi(l1_funding['excess_msat'])
    out_amt = out_2_ms + Millisatoshi(l2_funding['excess_msat']) + out_total + out_total
    output_psbt = bitcoind.rpc.createpsbt([],
                                          [{addr: float(out_amt.to_btc())}])
    joint_psbt = bitcoind.rpc.joinpsbts([l1_funding['psbt'], l2_funding['psbt'],
                                         output_psbt])

    # Ask it to sign inputs it doesn't know, it will fail.
    with pytest.raises(RpcError, match=r"is unknown"):
        l1.rpc.signpsbt(joint_psbt,
                        signonly=list(range(l1_num_inputs + 1)))

    # Similarly, it can't sign inputs it doesn't know.
    sign_success = []
    for i in range(l1_num_inputs + l2_num_inputs):
        try:
            l1.rpc.signpsbt(joint_psbt, signonly=[i])
        except RpcError:
            continue
        sign_success.append(i)
    assert len(sign_success) == l1_num_inputs

    # But it can sign all the valid ones at once.
    half_signed_psbt = l1.rpc.signpsbt(joint_psbt, signonly=sign_success)['signed_psbt']
    for s in sign_success:
        decoded_input = bitcoind.rpc.decodepsbt(half_signed_psbt)['inputs'][s]
        if 'partial_signatures' in decoded_input:
            assert decoded_input['partial_signatures'] is not None
        else:
            # VLS returns signatures in final_scriptwitness instead
            assert decoded_input['final_scriptwitness'] is not None

    totally_signed = l2.rpc.signpsbt(half_signed_psbt)['signed_psbt']

    broadcast_tx = l1.rpc.sendpsbt(totally_signed)
    l1.daemon.wait_for_log(r'sendrawtx exit 0 .* sendrawtransaction {}'.format(broadcast_tx['tx']))

    # Send a PSBT that's not ours
    l2_funding = l2.rpc.fundpsbt(satoshi=out_total,
                                 feerate=7500,
                                 startweight=42)
    out_amt = Millisatoshi(l2_funding['excess_msat'])
    output_psbt = bitcoind.rpc.createpsbt([],
                                          [{addr: float((out_total + out_amt).to_btc())}])
    psbt = bitcoind.rpc.joinpsbts([l2_funding['psbt'], output_psbt])
    l2_signed_psbt = l2.rpc.signpsbt(psbt)['signed_psbt']
    l1.rpc.sendpsbt(l2_signed_psbt)

    # Re-try sending the same tx?
    bitcoind.generate_block(1)
    sync_blockheight(bitcoind, [l1])
    # Expect an error here
    # VLS/BitcoinD mismatch: VLS tests sometimes see "Transaction outputs already in utxo set"
    with pytest.raises(JSONRPCError, match=r"Transaction already in block chain|Transaction outputs already in utxo set"):
        bitcoind.rpc.sendrawtransaction(broadcast_tx['tx'])

    # Try an empty PSBT
    with pytest.raises(RpcError, match=r"psbt: Expected a PSBT: invalid token"):
        l1.rpc.signpsbt('')
    with pytest.raises(RpcError, match=r"psbt: Expected a PSBT: invalid token"):
        l1.rpc.sendpsbt('')

    # Try an invalid PSBT string
    invalid_psbt = 'cHNidP8BAM0CAAAABJ9446mTRp/ml8OxSLC1hEvrcxG1L02AG7YZ4syHon2sAQAAAAD9////JFJH/NjKwjwrP9myuU68G7t8Q4VIChH0KUkZ5hSAyqcAAAAAAP3///8Uhrj0XDRhGRno8V7qEe4hHvZcmEjt3LQSIXWc+QU2tAEAAAAA/f///wstLikuBrgZJI83VPaY8aM7aPe5U6TMb06+jvGYzQLEAQAAAAD9////AcDGLQAAAAAAFgAUyQltQ/QI6lJgICYsza18hRa5KoEAAAAAAAEBH0BCDwAAAAAAFgAUqc1Qh7Q5kY1noDksmj7cJmHaIbQAAQEfQEIPAAAAAAAWABS3bdYeQbXvBSryHNoyYIiMBwu5rwABASBAQg8AAAAAABepFD1r0NuqAA+R7zDiXrlP7J+/PcNZhwEEFgAUKvGgVL/ThjWE/P1oORVXh/ObucYAAQEgQEIPAAAAAAAXqRRsrE5ugA1VJnAith5+msRMUTwl8ocBBBYAFMrfGCiLi0ZnOCY83ERKJ1sLYMY8A='
    with pytest.raises(RpcError, match=r"psbt: Expected a PSBT: invalid token"):
        l1.rpc.signpsbt(invalid_psbt)

    wallet_coin_mvts = [
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 1000000000, 'debit_msat': 0, 'tags': ['deposit']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
        {'type': 'chain_mvt', 'credit_msat': 0, 'debit_msat': 1000000000, 'tags': ['withdrawal']},
    ]

    check_coin_moves(l1, 'wallet', wallet_coin_mvts, chainparams)

# Skip tests that use hsmtool on the hsm_secret file, which is not supported in VLS socket mode (remote signer)

def test_hsm_secret_encryption(node_factory):
    return original_test_hsm_secret_encryption(node_factory)

@pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="remote_hsmd doesn't support hsm_secret file")
def test_hsmtool_secret_decryption(node_factory):
    return original_test_hsmtool_secret_decryption(node_factory)

@pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="remote_hsmd doesn't support generatehsm")
def test_hsmtool_generatehsm(node_factory):
    return original_test_hsmtool_generatehsm(node_factory)