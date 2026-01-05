from fixtures import *  # noqa: F401,F403

# Import all tests from CLN
from lightning.tests.test_runes import (
    test_createrune,
    test_createrune_per_restriction,
    test_showrunes,
    test_blacklistrune,
    test_badrune,
    test_checkrune,
    test_rune_pay_amount,
    test_commando_rune_migration,
    test_commando_blacklist_migration,
    test_missing_method_or_nodeid,
    test_rune_method_missing,
    test_invalid_restrictions,
    test_nonnumeric_uniqueid,
    test_showrune_id,
    test_id_migration,
    test_rune_error_messages,
    test_rune_bolt11_parse,
    test_rune_bolt12_parse,
)
