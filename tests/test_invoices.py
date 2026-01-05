from fixtures import *  # noqa: F401,F403

# Import all tests from CLN
from lightning.tests.test_invoices import (
    test_invoice,
    test_invoice_zeroval,
    test_invoice_weirdstring,
    test_invoice_preimage,
    test_invoice_routeboost,
    test_invoice_routeboost_private,
    test_invoice_expiry,
    test_waitinvoice,
    test_waitanyinvoice,
    test_signinvoice,
    test_waitanyinvoice_reversed,
    test_decode_unknown,
    test_amountless_invoice,
    test_listinvoices_filter,
    test_wait_invoices,
    test_invoice_deschash,
    test_listinvoices_index,
    test_unified_invoices,
    test_expiry_startup_crash,
    test_invoices_wait_db_migration,
    test_invoice_botched_migration,
)
