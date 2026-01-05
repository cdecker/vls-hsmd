from fixtures import *  # noqa: F401,F403

# Import all tests from CLN
from lightning.tests.test_renepay import (
    test_simple,
    test_direction_matters,
    test_shadow_routing,
    test_mpp,
    test_errors,
    test_pay,
    test_amounts,
    test_limits,
    test_hardmpp,
    test_self_pay,
    test_fee_allocation,
    test_htlc_max,
    test_previous_sendpays,
    test_fees,
    test_local_htlcmax0,
    test_htlcmax0,
    test_concurrency,
    test_privatechan,
    test_hardmpp2,
    test_description,
)
