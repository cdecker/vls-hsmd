# A C-Lightning hsmd replacement that connects to VLS

[![pipeline status](https://gitlab.com/lightning-signer/vls-hsmd/badges/main/pipeline.svg)](https://gitlab.com/lightning-signer/vls-hsmd/-/commits/main)

## First Time Setup

Follow the [First Time Setup Instructions](./SETUP.md).

## Running

Setup, configure, build and run the tests:

    make

Might need to increase open file limit if running all tests:

    ulimit -n 10000

Run tests:

    make -k test-all VLS_MODE=cln:socket

Using in-place VLS:

    make -k test-all VLS_MODE=cln:inplace

Run tests w/ VLS in permissive mode:

    make -k test-all VLS_MODE=cln:socket VLS_PERMISSIVE=1

Run a single test:

    make test-one TEST=tests/test_pay.py::test_pay
    make test-one TEST=tests/test_pay.py::test_pay VLS_MODE=cln:socket

Run a single test with native hsmd:

    make test-one TEST=tests/test_pay.py::test_pay VLS_MODE=cln:native

## Environment Variables

Moved to [`vls/contrib/howto/vls-env.md`](vls/contrib/howto/vls-env.md)

