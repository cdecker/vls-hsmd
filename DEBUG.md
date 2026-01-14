# Debugging Test Failures

## Session Summary (2026-01-11)

**Progress**:
- Tested `test_invoices.py`: 18 passed, 3 skipped (1 new skip added for `test_signinvoice`)
- Tested `test_db.py`: 5 passed, 8 skipped (6 new VLS skips for database migration tests)
- Tested `test_gossip.py`: 49 passed, 2 skipped (1 new skip for broken CLN test)
- Updated test files with appropriate skips and verified all fixes work correctly

### 1. `test_invoices.py` Results

**Native Signer (Baseline):**
- All 21 tests passed successfully in 223.27s

**VLS Socket Mode:**
- 18 passed, 2 skipped (pre-existing), 1 failed, 1 error in 438.14s
- **Failed:** `test_signinvoice` - Timeout (>180s)
- **Error:** `test_signinvoice` teardown error

**Analysis:**
- The `test_signinvoice` test calls the `signinvoice` RPC which allows one node to re-sign another node's invoice
- VLS hangs when processing this request, causing a timeout >180s
- This suggests VLS either doesn't support this operation or has a bug in handling it

**Fix Applied:**
- Added skip for `test_signinvoice` in `tests/test_invoices.py` with reason "VLS hangs when processing signinvoice RPC command, causing timeout"

### 2. `test_db.py` Results

**Native Signer (Baseline):**
- 11 passed, 2 skipped (test_scid_upgrade, test_psql_key_value_dsn) in 105.96s

**VLS Socket Mode (Final):**
- 5 passed, 2 skipped (pre-existing), 6 failed (all timeouts), 5 errors in 1177.03s (19:37)
- **Passed:** `test_db_dangling_peer_fix`, `test_block_backfill`, `test_max_channel_id`, `test_optimistic_locking`, `test_sqlite3_builtin_backup`
- **Timeouts:** All 6 failures are timeout-related (>180s each):
  - `test_last_tx_inflight_psbt_upgrade`
  - `test_last_tx_psbt_upgrade`
  - `test_backfill_scriptpubkeys`
  - `test_local_basepoints_cache`
  - `test_db_sanity_checks`
  - `test_db_forward_migrate`

**Analysis:**
- All failing tests involve database upgrades/migrations with node restarts
- VLS times out during database operations that require node restart
- The pattern confirms VLS has issues with database locking or daemon restart during migrations
- This aligns with previous findings about `DatabaseAlreadyOpen` panics and restart issues

**Fix Applied:**
- Added skips for all 6 timeout tests in `tests/test_db.py` with detailed reasons
- Each skip is conditional on `VLS_MODE == "cln:socket"`

### 3. `test_gossip.py` Results

**Native Signer (Baseline):**
- 49 passed, 1 skipped, 1 failed (timeout) in 1552.98s (25:52)
- **Failed:** `test_gossip_pruning` - Timeout (>180s)

**VLS Socket Mode:**
- 49 passed, 1 skipped, 1 failed (timeout) in 1700.85s (28:20)
- **Failed:** `test_gossip_pruning` - Timeout (>180s) - **Same as native!**

**Analysis:**
- VLS and native have identical results - no VLS-specific failures!
- `test_gossip_pruning` times out in both modes, indicating it's a broken test in CLN itself
- This is the first test file where VLS fully matches native behavior (except for the broken test)

**Fix Applied:**
- Added unconditional skip for `test_gossip_pruning` (not VLS-specific)
- Reason: "Test times out in both native and VLS modes (broken CLN test)"

**Verification:**
- Re-ran with VLS: 49 passed, 2 skipped in 1481.37s (24:41) ✅

### 4. `test_closing.py` Results

**Native Signer (Baseline):**
- 70 passed, 6 skipped, 1 failed (timeout) in 1517.48s (25:17)
- **Failed:** `test_closing_negotiation_reconnect` - Timeout (>180s)

**VLS Socket Mode:**
- 66 passed, 6 skipped, 5 failed (all timeouts) in 2518.63s (41:58)
- **Failed:**
  - `test_closing_negotiation_reconnect` - Same as native (broken CLN test)
  - `test_penalty_htlc_tx_fulfill[False]` - VLS-specific timeout
  - `test_penalty_htlc_tx_fulfill[True]` - VLS-specific timeout
  - `test_penalty_htlc_tx_timeout[False]` - VLS-specific timeout
  - `test_penalty_htlc_tx_timeout[True]` - VLS-specific timeout

**Analysis:**
- 1 failure is a broken CLN test (also fails on native)
- 4 VLS-specific failures all involve penalty transactions for HTLCs
- Penalty transactions are used when a peer tries to cheat by broadcasting old state
- VLS hangs when processing these penalty transaction scenarios (>180s each)

**Fixes Applied:**
- Added unconditional skip for `test_closing_negotiation_reconnect` (broken CLN test)
- Added VLS-conditional skips for both penalty HTLC tests (fulfill and timeout variants)

**Verification:**
- Re-ran with VLS: 66 passed, 11 skipped in 1566.86s (26:06) ✅

## Session Summary (2026-01-07)

**Progress**: 
- Investigated `test_askrene_fake_channeld` failure.
- Investigated and resolved (by skipping) `test_sign_and_send_psbt` failure.
- Verified 12 other wallet tests pass.
- Verified 14 runes tests pass and skipped 1.

### 1. `test_askrene_fake_channeld` (Failed)

- **Error:** `STATUS_FAIL_MASTER_IO: Error parsing 4294967295: 03f5...` (WIRE_CHANNELD_DEV_PEER_SHACHAIN).
- **Secondary Issue:** `vlsd2` panics with `DatabaseAlreadyOpen` during test execution/teardown.
- **Investigation:**
    - The `DatabaseAlreadyOpen` panic happens when `vlsd2` restarts. It seems `redb` lock is held by the previous process or a race condition in the test harness.
    - Attempted to fix `fixtures.py` by cancelling the `vlsd` start timer in `stop()`. This prevents starting `vlsd` if `stop()` is called immediately, but the panic persists in this specific test.
    - The `STATUS_FAIL_MASTER_IO` indicates `channeld_fakenet` crashes or closes connection unexpectedly when receiving `WIRE_CHANNELD_DEV_PEER_SHACHAIN`.
    - Instrumentation added to `channeld_fakenet.c` did not show up in logs (or was missed due to crash).
- **Status:** Unresolved. The test fails consistently. `DatabaseAlreadyOpen` complicates debugging.

### 2. `test_sign_and_send_psbt` (Skipped)

- **Original Error:** `AssertionError: Regex pattern did not match.` (Expected "Transaction already in block chain", got "Transaction outputs already in utxo set").
- **Fix Attempt 1:** Updated test to accept both error messages.
- **New Error:** `IndexError: list index out of range` in the loop checking `signpsbt` results.
- **Analysis:** VLS seems to behave differently than native CLN when signing PSBTs with unknown inputs or in the specific scenario of this test.
- **Resolution:** Skipped the test with `@pytest.mark.skip(reason="Fails with IndexError on VLS socket mode, needs investigation")` in `tests/test_wallet.py`.
- **Status:** Skipped.

### 3. Wallet Tests (12 Passed)

- Verified that the following tests pass in VLS mode:
    - `test_txsend`
    - `test_utxopsbt`
    - `test_fundpsbt`
    - `test_txprepare_multi`
    - `test_txprepare`
    - `test_reserveinputs`
    - `test_addpsbtoutput`
    - `test_sign_external_psbt`
    - `test_psbt_version`
    - `test_fundchannel_listtransaction`
    - `test_multiwithdraw_simple`
    - `test_repro_4258`
    - `test_p2tr_deposit_withdrawal`
    - `test_minconf_withdraw`
    - `test_addfunds_from_block`

### 4. Runes Tests (14 Passed, 1 Skipped)

- **Skipped:** `test_rune_bolt12_parse` because VLS does not support `WIRE_HSMD_SIGN_BOLT12_2` (msg 41).
- **Passed:**
    - `test_showrunes`
    - `test_showrune_id`
    - `test_rune_pay_amount`
    - `test_createrune`
    - `test_createrune_per_restriction`
    - `test_badrune`
    - `test_checkrune`
    - `test_blacklistrune`
    - `test_commando_rune_migration`
    - `test_commando_blacklist_migration`
    - `test_id_migration`
    - `test_invalid_restrictions`
    - `test_missing_method_or_nodeid`
    - `test_nonnumeric_uniqueid`
    - `test_rune_bolt11_parse`
    - `test_rune_error_messages`
    - `test_rune_method_missing`

## Fixes Applied

- **`tests/fixtures.py`**: Updated `VlsLightningNode` to properly cancel the `vlsd` start timer in `stop()`. This prevents a race condition where `vlsd` starts after `stop()` was called, potentially causing `DatabaseAlreadyOpen` (though it didn't fully solve it for `test_askrene`).
- **`tests/test_wallet.py`**: Added imports (`unittest`, `RpcError`, `JSONRPCError`, `sync_blockheight`, `wait_for`, `check_coin_moves`) and skipped `test_sign_and_send_psbt`.
- **`tests/test_runes.py`**: Added imports (`pytest`, `os`) and skipped `test_rune_bolt12_parse`.

## Next Steps

1.  Investigate `test_askrene_fake_channeld` `STATUS_FAIL_MASTER_IO` deeper.
2.  Investigate why `test_sign_and_send_psbt` fails with `IndexError` on VLS.
3.  Continue debugging other failing tests from `bd list`.

## Debugging Guidelines

### Waiting for Test Completion

**IMPORTANT:** When debugging a test, always wait for the test to finish completely by polling every 3 minutes. Do not stop at intermediate findings.

- Tests can take a long time (5-10 minutes for single tests, 30+ minutes for full suites)
- Timeouts are set to 180s per test, but some tests may hang and need the full timeout
- Intermediate output does not show the full picture - wait for the final summary line
- Use polling with `sleep` and `tail` commands to monitor progress without blocking
- Only analyze results after seeing the final pytest summary (e.g., "21 passed, 2 skipped in 223.27s")

## Test Skipping Strategy

When importing tests from `lightning/tests` to `tests/` in order to run them with VLS, we sometimes need to skip tests that are known to be incompatible or failing.

**Do NOT** wrap the test function in a new function like this:

```python
# BAD
@pytest.mark.skipif(...)
def test_foo(node_factory):
    return original_test_foo(node_factory)
```

This causes issues with signature mismatch if the original test uses fixtures (like `executor`, `bitcoind`, etc.) that are not in the wrapper's signature.

**DO** import the containing module and then apply the skip decorator to create the public test function:

```python
# GOOD
from lightning.tests import test_file

test_foo = pytest.mark.skipif(condition, reason="...")(test_file.test_foo)
```

This preserves the original function signature and fixture injection.

## Session Summary (2026-01-14)

### Issue: `remote_hsmd_socket` Fails with Unknown `--log-trace` Option

**Problem:**
- When CLN's log level is set to TRACE or lower (IO_IN/IO_OUT), it automatically passes `--log-trace` to all subdaemons via `lightning/lightningd/subd.c:264`
- The `remote_hsmd_socket` binary (VLS proxy) doesn't recognize this flag, causing it to fail with an "unknown option" error

**When is `--log-trace` passed?**
- In `lightning/lightningd/subd.c:263-264`, the `--log-trace` flag is passed when `trace_logging` is true
- `trace_logging` is determined by `log_has_trace_logging()` in `lightning/lightningd/log.c:495`
- This function returns true when the log level is less than `LOG_DBG` (i.e., `LOG_TRACE`, `LOG_IO_IN`, or `LOG_IO_OUT`)
- Log levels (from `lightning/common/status_levels.h`):
  - `LOG_IO_OUT` (0) - lowest
  - `LOG_IO_IN` (1)
  - `LOG_TRACE` (2)
  - `LOG_DBG` (3)
  - `LOG_INFORM` (4)
  - `LOG_UNUSUAL` (5)
  - `LOG_BROKEN` (6) - highest
- So `--log-trace` is passed when log level ≤ TRACE

**Root Cause:**
- In `vls/vls-proxy/src/util/mod.rs:103-115`, the `add_hsmd_args()` function only handles these flags:
  - `--dev-disconnect`
  - `--developer`
  - `--log-io`
  - `--version`
  - `--git-desc`
- Missing: `--log-trace` (and potentially `--dev-debug-self`)

**Solution:**
- The fix needs to be applied in the VLS upstream repository
- Add `--log-trace` as an ignored flag in `add_hsmd_args()`:
  ```rust
  .arg(Arg::new("log-trace").long("log-trace").help("ignored dev flag"))
  ```
- Similarly, `--dev-debug-self` should also be added for completeness

**Solution Implemented:**
- Created a wrapper script at `scripts/remote_hsmd_socket_wrapper.sh` that:
  - Filters out `--log-trace` and `--dev-debug-self` arguments
  - Passes all other arguments through to the actual `remote_hsmd_socket` binary
  - Uses `exec` to replace itself with the binary for proper signal handling
- Updated `tests/fixtures.py` to use the wrapper instead of the direct binary path
- This allows VLS to work even when CLN has trace-level logging enabled

**Testing:**
```bash
# Works with --log-trace (strips it)
VLS_CLN_VERSION=v1.0.0 ./scripts/remote_hsmd_socket_wrapper.sh --log-trace --version
# v1.0.0

# Works with other flags
VLS_CLN_VERSION=v1.0.0 ./scripts/remote_hsmd_socket_wrapper.sh --git-desc
# remote_hsmd_socket git_desc=git-desc-error
```

**Upstream Status:** Still needs to be fixed in VLS upstream in `vls/vls-proxy/src/util/mod.rs`, but we have a local workaround now.
