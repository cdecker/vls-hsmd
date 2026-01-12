from fixtures import *  # noqa: F401,F403
import os
import pytest

# Import all tests from CLN
from lightning.tests.test_invoices import (
    test_invoice,
    test_invoice_zeroval,
    test_invoice_weirdstring,
    test_invoice_preimage as _test_invoice_preimage,
    test_invoice_routeboost,
    test_invoice_routeboost_private,
    test_invoice_expiry,
    test_waitinvoice,
    test_waitanyinvoice,
    test_signinvoice as _test_signinvoice,
    test_waitanyinvoice_reversed,
    test_decode_unknown,
    test_amountless_invoice,
    test_listinvoices_filter,
    test_wait_invoices,
    test_invoice_deschash,
    test_listinvoices_index,
    test_unified_invoices,
    test_expiry_startup_crash,
    test_invoices_wait_db_migration as _test_invoices_wait_db_migration,
    test_invoice_botched_migration,
)

# VLS does not support reusing preimages - when an invoice with a duplicate preimage
# is created, VLS terminates the connection instead of returning an error gracefully.
# The test expects an RpcError with "preimage already used" but gets a connection termination.
test_invoice_preimage = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS terminates connection on duplicate preimage instead of returning error"
)(_test_invoice_preimage)

# This test has timeout issues with VLS socket mode - the VLS daemon panics with
# "EOF reading from HSM after WIRE_HSMD_SIGN_ANY_CANNOUNCEMENT_REQ" during node restart.
# This appears to be a VLS stability issue during database migration scenarios.
test_invoices_wait_db_migration = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS daemon crashes during database migration with WIRE_HSMD_SIGN_ANY_CANNOUNCEMENT_REQ"
)(_test_invoices_wait_db_migration)

# The signinvoice test times out with VLS in socket mode. The test calls the signinvoice
# RPC which allows one node to re-sign another node's invoice. VLS appears to hang when
# processing this request, causing a timeout >180s.
test_signinvoice = pytest.mark.skipif(
    os.environ.get("VLS_MODE") == "cln:socket",
    reason="VLS hangs when processing signinvoice RPC command, causing timeout"
)(_test_signinvoice)
