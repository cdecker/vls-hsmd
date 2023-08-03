
#### Install Dependencies

Update PATH:

    export PATH=$PATH:~/.local/bin

On Debian:

    sudo apt-get update
    sudo apt-get install -y \
      autoconf automake build-essential git libtool libgmp-dev libsqlite3-dev \
      python3 python3-pip net-tools zlib1g-dev libsodium-dev gettext \
      python3-mako \
      libprotobuf-c-dev \
      protobuf-compiler protobuf-compiler-grpc libgrpc++-dev pkg-config \
      curl

On Fedora:

    sudo dnf update -y && \
      sudo dnf groupinstall -y \
              'C Development Tools and Libraries' \
              'Development Tools' && \
      sudo dnf install -y \
              clang \
              gettext \
              git \
              gmp-devel \
              libsq3-devel \
              python3-devel \
              python3-pip \
              python3-setuptools \
              net-tools \
              valgrind \
              wget \
              zlib-devel \
              libsodium-devel \
              python3-mako \
              protobuf-compiler protobuf-devel grpc-devel grpc-plugins \
              perl

On Both:

    pip3 install --upgrade pip
    pip3 install --user poetry
    
    # These are currently touchy about versions (2022-05-02)
    pip3 install --user mistune==0.8.4
    pip3 install --user mrkd==0.2.0


#### Install Rust

You can probably skip this part if you already use rust ...

Directions from (https://www.rust-lang.org/learn/get-started):

    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    # accept the defaults ...
    source $HOME/.cargo/env


#### Install Bitcoind

If you already have `bitcoind` and `bitcoin-cli` installed and in your path you
can skip this part.

On Debian:

    sudo apt-get install -y snapd
    sleep 30
    sudo snap install bitcoin-core
    # Snap does some weird things with binary names; you'll
    # want to add a link to them so everything works as expected
    sudo ln -s /snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/

On Fedora:

    sudo dnf install -y snapd
    sleep 30
    sudo snap install bitcoin-core
    # Snap does some weird things with binary names; you'll
    # want to add a link to them so everything works as expected
    sudo ln -s /var/lib/snapd/snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/


#### Checkout VLS/CLN Integration Repository

Change directories to a good place for the development tree, example:

    mkdir ~/lightning-signer && cd ~/lightning-signer

Checkout the VLS/CLN Integration Repository:

    git clone https://gitlab.com/lightning-signer/vls-hsmd.git && cd vls-hsmd

Choose a branch:

    git checkout main

Recursively checkout submodules:

    git submodule update --init --recursive

Enable githooks

    ./scripts/enable-githooks


#### Build and Run

Build everything

    make build

Run a test

    make test-one TEST=tests/test_pay.py::test_pay

See the [README](./README.md) for more examples ...
