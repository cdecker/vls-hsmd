## Bitcoind Setup

You can skip this entirely if you already have bitcoin installed as a service.

You can skip the service configuration steps if you are not running as a
service, but you still need the binaries to run integration testing.

### Install Binaries

Install the bitcoind binaries on the `CLNHOST`.

On Debian:
```
sudo apt-get install -y snapd
sleep 30
sudo snap install bitcoin-core
# Snap does some weird things with binary names; you'll
# want to add a link to them so everything works as expected
sudo ln -s /snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/
```

On Fedora:
```
sudo dnf install -y snapd
sleep 30
sudo snap install bitcoin-core
# Snap does some weird things with binary names; you'll
# want to add a link to them so everything works as expected
sudo ln -s /var/lib/snapd/snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/
```

### Configure Service

Configure the bitcoind service on the `CLNHOST`.

Add `bitcoin` user and group:
```
sudo /usr/sbin/groupadd bitcoin
sudo /usr/sbin/useradd -g bitcoin -c "bitcoin" -m bitcoin
```

Install sample config:
```
sudo mkdir -p /home/bitcoin/.bitcoin
sudo cp ~/lightning-signer/vls-hsmd/howto/artifacts/bitcoin.conf /home/bitcoin/.bitcoin
sudo chown -R bitcoin:bitcoin  /home/bitcoin/.bitcoin
```

Edit the config file, change the `rpcpassword` to something random:
```
sudo vi /home/bitcoin/.bitcoin
```

Install systemd unit file:
```
sudo cp ~/lightning-signer/vls-hsmd/howto/artifacts/bitcoind-testnet.service /lib/systemd/system/
sudo systemctl daemon-reload
```

Enable the  service for automatic start on system boot:
```
sudo systemctl enable bitcoind-testnet
```

If you want to start the service now:
```
sudo systemctl start bitcoind-testnet
```

View status:
```
sudo systemctl status bitcoind-testnet
```
