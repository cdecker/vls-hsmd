import os
import pytest
from fixtures import *  # noqa: F401,F403

# Import all tests from CLN - tests are identical
from lightning.tests.test_db import (
    test_db_dangling_peer_fix,
    test_block_backfill,
    test_max_channel_id,
    test_scid_upgrade as _test_scid_upgrade,
    test_last_tx_inflight_psbt_upgrade as _test_last_tx_inflight_psbt_upgrade,
    test_last_tx_psbt_upgrade as _test_last_tx_psbt_upgrade,
    test_backfill_scriptpubkeys as _test_backfill_scriptpubkeys,
    test_optimistic_locking,
    test_psql_key_value_dsn,
    test_local_basepoints_cache as _test_local_basepoints_cache,
    test_sqlite3_builtin_backup,
    test_db_sanity_checks as _test_db_sanity_checks,
    test_db_forward_migrate as _test_db_forward_migrate,
)

# Skip tests that don't interact with the signer
test_scid_upgrade = pytest.mark.skip("Does not interact with signer, calls lightningd directly")(_test_scid_upgrade)

# VLS has timeout issues with database upgrade tests that involve node restarts.
# These tests time out (>180s) when running with VLS in socket mode, likely due to
# issues with database locking or VLS daemon restart handling during migrations.
test_last_tx_inflight_psbt_upgrade = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out during database upgrade with PSBT inflight transactions"
)(_test_last_tx_inflight_psbt_upgrade)

test_last_tx_psbt_upgrade = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out during database upgrade with PSBT transactions"
)(_test_last_tx_psbt_upgrade)

test_backfill_scriptpubkeys = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out during database upgrade when backfilling scriptpubkeys"
)(_test_backfill_scriptpubkeys)

test_local_basepoints_cache = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out during database upgrade with local basepoints cache"
)(_test_local_basepoints_cache)

test_db_sanity_checks = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out during database sanity checks test"
)(_test_db_sanity_checks)

test_db_forward_migrate = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS times out during forward database migration test"
)(_test_db_forward_migrate)
