# A C-Lightning hsmd replacement that connects to VLS

[![pipeline status](https://gitlab.com/lightning-signer/vls-hsmd/badges/main/pipeline.svg)](https://gitlab.com/lightning-signer/vls-hsmd/-/commits/main)

## First Time Setup

Follow the [First Time Setup Instructions](./SETUP.md).

## Running

Setup, configure, build and run the standard tests:

    make

Both standard and experimental-features tests:

    make -k test-all VLS_MODE=cln:standalone

Using in-place VLS:

    make -k test-all VLS_MODE=cln:inplace

Using socket connection to VLS:

    make -k test-all VLS_MODE=cln:socket

Summarize results:

    scripts/summary standard.log
    scripts/summary experimental.log

Run a single test:

    make config-experimental
    make test-one TEST=tests/test_pay.py::test_pay
    make test-one TEST=tests/test_pay.py::test_pay VLS_MODE=cln:inplace
    make test-one TEST=tests/test_pay.py::test_pay VLS_MODE=cln:socket

Run a single test with native hsmd:

    make test-one TEST=tests/test_pay.py::test_pay VLS_MODE=cln:native
