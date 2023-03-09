## Clone CLN+VLS Integration Repository

Choose somewhere to clone tree:
```
mkdir ~/lightning-signer && cd ~/lightning-signer
```

Clone tree, select branch, update:
```
git clone https://gitlab.com/lightning-signer/vls-hsmd.git && cd vls-hsmd
git checkout <branch-tag-or-main>
git submodule update --init --recursive
```

One-time setup stuff:
```
./scripts/enable-githooks
```

Check if an integration test works:
```
make test-one TEST=tests/test_pay.py::test_pay
```
