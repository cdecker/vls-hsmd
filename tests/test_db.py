import unittest
from fixtures import *  # noqa: F401,F403

# Import all tests from CLN - tests are identical
from lightning.tests.test_db import (
    test_db_dangling_peer_fix,
    test_block_backfill,
    test_max_channel_id,
    test_scid_upgrade as _test_scid_upgrade,
    test_last_tx_inflight_psbt_upgrade,
    test_last_tx_psbt_upgrade,
    test_backfill_scriptpubkeys,
    test_optimistic_locking,
    test_psql_key_value_dsn,
    test_local_basepoints_cache,
    test_sqlite3_builtin_backup,
    test_db_sanity_checks,
    test_db_forward_migrate,
)

# Skip tests that don't interact with the signer
test_scid_upgrade = unittest.skip("Does not interact with signer, calls lightningd directly")(_test_scid_upgrade)
