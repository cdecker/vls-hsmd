# A C-Lightning hsmd replacement that connects to VLS

[![pipeline status](https://gitlab.com/lightning-signer/vls-hsmd/badges/main/pipeline.svg)](https://gitlab.com/lightning-signer/vls-hsmd/-/commits/main)

## Running

Setup, configure, build and run the standard tests:

    make

Both standard and experimental-features tests:

    make -k test-all

Summarize results:

    scripts/summary standard.log
    scripts/summary experimental.log

Run a single test:

    make config-experimental
    make test-one test=tests/test_pay.py::test_pay
