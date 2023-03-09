## Update CLN+VLS Software

This procedure presumes you've already performed the [One Time Setup](one-time-setup.md)

This procedure refers to the machine running the Core Lightning Node
and VLS proxies as the `CLNHOST`.  This procedure refers to the
machine running the VLS signer as the `VLSHOST`.  In development these
hosts may be the same.

### Stop Daemons

If you are running the software you need to quiesce it.

On the `CLNHOST`:
```
sudo systemctl stop cln-testnet
ps uaxgwww | grep cln
```

On the `VLSHOST` [if you are running in `SOCKET` mode]:
```
sudo systemctl stop vls-testnet
ps uaxgwww | grep vls
```

If you are running the signer on an STM32 in `SERIAL` mode no action
is required, the signer can be left idle.

### Update Software

#### Checkout desired branch/tag

Choose a `vls-hsmd`  version or branch, if unsure use `main`
```
cd ~/lightning-signer/vls-hsmd
git fetch --recurse-submodules
git checkout <your-branch-or-main>
git pull
make setup
```

#### Build Software
```
cd ~/lightning-signer/vls-hsmd && make build-standard
```

#### Install Software

Install CLN components:
```
cd ~/lightning-signer/vls-hsmd/lightning
poetry run make
sudo make install
```

Install VLS proxies on the `CLNHOST`:
```
sudo cp ~/lightning-signer/vls-hsmd/vls/target/debug/remote_hsmd_serial \
    /usr/local/libexec/c-lightning/
sudo cp ~/lightning-signer/vls-hsmd/vls/target/debug/remote_hsmd_socket \
    /usr/local/libexec/c-lightning/
```

Install the VLS signer on the `VLSHOST` if you are running in `SOCKET` mode:
```
sudo cp ~/lightning-signer/vls-hsmd/vls/target/debug/vlsd2 /usr/local/bin
```

Update `~cln/.lightning/testnet-env` to CLN version:
```
sudo su cln
cd ~cln/.lightning/
grep -v GREENLIGHT_VERSION testnet-env > testnet-env.new &&
  echo "GREENLIGHT_VERSION=`lightningd --version`" >> testnet-env.new &&
  mv testnet-env.new testnet-env
```

[Flash the STM32 Signer](./stm32-flash.md) if you are running in `SERIAL` mode.

### Contemplate State Changes

Generally, you don't do anything.  But if you did want to
change/erase/revert something this is a good time to do it.

If you do want to alter CLN state on the `CLNHOST`:
```
sudo su cln
cd /home/cln/.lightning
# do stuff
exit
```

If you do want to alter VLS signer state on the `VLSHOST`:
```
sudo su vls
cd /home/vls/.lightning-signer
# do stuff
exit
```

If you are using a STM32 signer in `SERIAL` mode you can hold the blue
button while resetting with the black button to enter setup mode.  You
can also mount the sdcard in a development machine and view/alter the
state.

### Start Daemons

If you are running the signer on an STM32 press the black button to
reset it.  The signer will disply "waiting for node" when it is ready.

On the `VLSHOST` [if you are running in `SOCKET` mode]:
```
sudo systemctl start vls-testnet
```

On the `CLNHOST`:
```
sudo systemctl start cln-testnet
```

Individual status checks:
```
sudo systemctl status cln-testnet
sudo systemctl status vls-testnet
```

Quick summary status:
```
for svc in \
bitcoind-testnet \
cln-testnet \
vls-testnet \
; do SYSTEMD_COLORS=1 systemctl status $svc | head -n 3; done
```
