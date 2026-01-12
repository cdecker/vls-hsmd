FROM ubuntu:25.04
ENV HOME=/root/
ENV RUST_VERSION=1.87.0
ENV PATH=$PATH:/root/.local/bin/:/root/.local/share/uv/tools:/root/.cargo/bin/
ENV UV_PYTHON=3.10
ENV DEBIAN_FRONTEND=noninteractive
ENV BITCOIN_VERSION=25.0

RUN apt-get update && \
    apt-get install -qq -yy --no-install-recommends \
      autoconf \
      automake \
      binfmt-support \
      build-essential \
      ca-certificates \
      clang \
      cppcheck \
      curl \
      docbook-xml \
      eatmydata \
      gcc-aarch64-linux-gnu \
      gcc-arm-linux-gnueabihf \
      gcc-arm-none-eabi \
    gettext \
jq \
      git \
      libc6-dev-arm64-cross \
      libc6-dev-armhf-cross \
      libgmp-dev \
      libgrpc++-dev \
      libpq-dev \
      libprotobuf-c-dev \
      libsodium-dev \
      libsqlite3-dev \
      libtool \
      libxml2-utils \
      locales \
      net-tools \
      pkg-config \
      postgresql \
      protobuf-compiler \
      protobuf-compiler-grpc \
      python-is-python3 \
      python3 \
      python3-dev \
      python3-venv \
      python3-pip \
      shellcheck \
      software-properties-common \
      sudo \
      sudo \
      tcl \
      tzdata \
      unzip \
      valgrind \
      wget \
      xsltproc \
      zlib1g-dev \
    && apt-get clean

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- \
      -y --default-toolchain ${RUST_VERSION} --profile minimal
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN curl -v -L "https://github.com/mozilla/sccache/releases/download/v0.10.0/sccache-v0.10.0-x86_64-unknown-linux-musl.tar.gz" > /tmp/sccache.tar.gz \
    && ls -lha /tmp/ \
    && tar -xvzf /tmp/sccache.tar.gz --strip-components=1 --wildcards '*/sccache' \
    && mv sccache /usr/local/bin/ \
    && chmod +x /usr/local/bin/sccache
RUN cd /tmp && \
    wget "https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/bitcoin-${BITCOIN_VERSION}-x86_64-linux-gnu.tar.gz" -O bitcoin.tar.gz && \
    tar -xvzf bitcoin.tar.gz && \
    mv /tmp/bitcoin-$BITCOIN_VERSION/bin/bitcoin* /usr/local/bin/ && \
    rm -rf bitcoin.tar.gz /tmp/bitcoin-$BITCOIN_VERSION

RUN mkdir /repo
WORKDIR /repo
RUN git config --global --add safe.directory /repo
#COPY . /repo
RUN uv tool install poetry==1.8
#RUN /root/.local/bin/uv sync && /root/.local/bin/uv pip install poetry==1.8

#COPY remote_hsmd_inplace remote_hsmd_inplace
#COPY scripts scripts
#COPY .gitmodules .gitmodules
#COPY .git .git
#ENV SUBDAEMON hsmd:remote_hsmd_inplace

