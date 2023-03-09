## Install Dependencies

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
