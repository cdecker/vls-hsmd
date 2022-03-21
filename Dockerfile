FROM ubuntu

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qq -yy --no-install-recommends git ca-certificates sudo tzdata python3 python3-pip python3-setuptools python3-dev python-is-python3 autoconf automake binfmt-support build-essential clang cppcheck docbook-xml eatmydata gcc-aarch64-linux-gnu gcc-arm-linux-gnueabihf gcc-arm-none-eabi gettext git libc6-dev-arm64-cross libc6-dev-armhf-cross libgmp-dev libpq-dev libprotobuf-c-dev libsqlite3-dev libtool libxml2-utils locales net-tools postgresql python-pkg-resources python3 python3-dev python3-pip python3-setuptools qemu qemu-system-arm qemu-user-static shellcheck software-properties-common sudo tcl unzip valgrind wget xsltproc zlib1g-dev && apt-get clean
RUN pip3 install --upgrade pip
