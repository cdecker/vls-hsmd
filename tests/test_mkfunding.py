from fixtures import *  # noqa: F401,F403

# Import all tests and constants from CLN - tests are identical
from lightning.tests.test_mkfunding import (
    TIMEOUT,
    EXECUTABLE,
    INPUT_TXID,
    INPUT_TXOUTPUT,
    INPUT_AMOUNT,
    FEERATE_PER_KW,
    INPUT_PRIVKEY,
    LOCAL_FUNDING_PRIVKEY,
    REMOTE_FUNDING_PRIVKEY,
    subprocess_run,
    test_mkfunding_bad_usage,
    test_mkfunding_bad_input_txid,
    test_mkfunding_bad_input_amount,
    test_mkfunding_bad_input_privkey,
    test_mkfunding_bad_local_funding_privkey,
    test_mkfunding_bad_remote_funding_privkey,
    test_mkfunding_bad_privkeys,
    test_mkfunding_bad_cantaffordfee,
    test_mkfunding_good_noabort,
)
