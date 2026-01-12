from fixtures import *  # noqa: F401,F403
import pytest
import os

# Import all tests from CLN
from lightning.tests.test_runes import (
    test_showrunes,
    test_showrune_id,
    test_createrune,
    test_createrune_per_restriction,
    test_rune_pay_amount,
    test_badrune,
    test_checkrune,
    test_blacklistrune,
    test_commando_rune_migration,
    test_commando_blacklist_migration,
    test_id_migration,
    test_invalid_restrictions,
    test_missing_method_or_nodeid,
    test_nonnumeric_uniqueid,
    test_rune_bolt11_parse,
    test_rune_bolt12_parse as _test_rune_bolt12_parse,
    test_rune_error_messages,
    test_rune_method_missing,
)

test_rune_bolt12_parse = pytest.mark.skipif(os.environ.get("VLS_MODE") == "cln:socket", reason="VLS does not support WIRE_HSMD_SIGN_BOLT12_2 (msg 41)")(_test_rune_bolt12_parse)