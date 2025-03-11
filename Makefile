
VLS_MODE ?= cln:socket
TIMEOUT ?= 300
VALGRIND ?= 0
TEST ?= tests/test_pay.py::test_pay
PREFIX ?= /usr/local

CARGO_TARGET_DIR ?= "$(shell pwd)/vls/target/"
RUST_TARGET = "debug"
CARGO_BINDIR = "$(CARGO_TARGET_DIR)/$(RUST_TARGET)"
JPAR ?= $(shell nproc)
TPAR ?= $(JPAR)

ifeq ("$(VLS_MODE)","cln:inplace")
	SUBDAEMON:="hsmd:$(CARGO_BINDIR)/remote_hsmd_inplace"
else ifeq ("$(VLS_MODE)","cln:socket")
	SUBDAEMON:="hsmd:$(CARGO_BINDIR)/remote_hsmd_socket"
else ifeq ("$(VLS_MODE)","cln:native")
	SUBDAEMON:="hsmd:lightning_hsmd"
else ifeq ("$(VLS_MODE)","cln:serial")
    # embedded for node 1, native for the rest
	SUBDAEMON:="hsmd:$(CARGO_BINDIR)/remote_hsmd_serial,hsmd:$(CARGO_BINDIR)/lightning_hsmd"
endif

GITDESC:=$(shell git describe --tags --long --always --match='v*.*')

all: test

test-all: test

list-versions:
	@echo "vls-hsmd ($(shell git describe --tags --long --always --match='v*.*' --dirty))"
	@git submodule status

setup:	check-git-version .setup-complete

check-git-version:
ifneq ("$(wildcard .setup-complete)", "")
  ifneq ($(GITDESC),$(shell cat .setup-complete))
	@echo "git hash changed, rerunning setup"
	rm .setup-complete
  endif
endif

config:	setup .config
config:	CFGFLAGS=

build:	config

test:	build

.setup-complete: ./scripts/setup-remote-hsmd
	git submodule update --init --recursive
	./scripts/enable-githooks
	./scripts/setup-remote-hsmd
	mkdir -p $(PWD)/bin
	(cd bin && ln -fs ../vls/target/debug/vlsd2)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_socket)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_serial)
	(cd bin && ln -fs ../vls/lightning-storage-server/target/debug/lssd)
	echo "$(GITDESC)" > $@
	make list-versions

.config:
	rm -f .config
	(cd lightning/external/lowdown && ./configure) # WORKAROUND
	cd lightning \
		&& make distclean \
		&& poetry install \
		&& ./configure $(CFGFLAGS)
	touch $@

build:	config
	cd lightning && poetry run make -j$(JPAR)
	cd vls && cargo build --bins --features developer $(VLS_BUILDARGS)
	cd vls/lightning-storage-server && cargo build --bins $(LSS_BUILDARGS)

# unfortunately this cannot depend on build because frequently run as
# sudo root and will not have poetry available
install:
	(cd lightning && make install PREFIX=$(PREFIX))
	cp vls/target/debug/remote_hsmd_serial $(PREFIX)/libexec/c-lightning/
	cp vls/target/debug/remote_hsmd_socket $(PREFIX)/libexec/c-lightning/
	cp vls/target/debug/vlsd2 $(PREFIX)/bin
	@$(PREFIX)/bin/lightningd --version
	@$(PREFIX)/libexec/c-lightning/remote_hsmd_serial --git-desc
	@$(PREFIX)/libexec/c-lightning/remote_hsmd_socket --git-desc
	@$(PREFIX)/bin/vlsd2 --git-desc

install-testnet: build
	sudo ./scripts/install-version testnet

# use a timestamp version test results directory
TEST_SUBDIR := TEST-$(shell date +"%Y%m%d-%H%M%S")

test:	RUN_DIR ?= /tmp
test:	TEST_DIR = $(abspath $(RUN_DIR)/$(TEST_SUBDIR))
test:	LOGFILE = ALL.log
test:	LATEST = ./LATEST-TEST-ALL
test:	check-subdaemon
	-. scripts/setup-env \
		&& echo Running all tests in $(TEST_DIR) \
		&& mkdir -p $(TEST_DIR) \
		&& rm -f  $(LATEST) \
		&& ln -s $(TEST_DIR) $(LATEST) \
	    && cd lightning \
		&& export \
			DEVELOPER=1 \
			SUBDAEMON=$(SUBDAEMON) \
			VALGRIND=$(VALGRIND) \
			TIMEOUT=$(TIMEOUT) \
			TEST_DIR=$(TEST_DIR) \
		&& printenv >  $(TEST_DIR)/ENV.log \
		&& poetry run make pytest -j$(JPAR)\
			VALGRIND=$(VALGRIND) \
			PYTEST_MOREOPTS="--timeout=$(TIMEOUT) --timeout_method=signal -vvv" \
			PYTEST_PAR=$(TPAR) \
		2>&1 | tee $(TEST_DIR)/$(LOGFILE)
		scripts/prune-test-dir $(TEST_DIR)
		vls/contrib/howto/assets/logsum $(TEST_DIR)

clean:
	rm -f .config
	cd vls && cargo clean
	cd lightning && make distclean

test-one:	RUN_DIR ?= $(PWD)
test-one:	TEST_DIR = $(abspath $(RUN_DIR)/$(TEST_SUBDIR))
test-one:	LOGFILE = ONE.log
test-one:	LATEST = ./LATEST-TEST-ONE
test-one:	check-subdaemon check-test-one build
	. scripts/setup-env \
		&& echo Running $(TEST) in $(TEST_DIR) \
		&& mkdir -p $(TEST_DIR) \
		&& rm -f  $(LATEST) \
		&& ln -s $(TEST_DIR) $(LATEST) \
		&& cd lightning \
		&& export \
			DEVELOPER=1 \
			SUBDAEMON=$(SUBDAEMON) \
			VALGRIND=$(VALGRIND) \
			TIMEOUT=$(TIMEOUT) \
			TEST_DIR=$(TEST_DIR) \
		&& poetry run ../scripts/run-one-test $(TEST) \
		2>&1 | tee $(TEST_DIR)/$(LOGFILE)
		vls/contrib/howto/assets/logsum $(TEST_DIR)

check-subdaemon:
	@if test -z $(SUBDAEMON); then echo "unknown VLS_MODE $(VLS_MODE)"; exit 1; fi

check-test-one:
	@if test -z $(TEST); then echo "usage: make test-one TEST=<your-test-here>"; exit 1; fi

.PHONY : all test-all setup clean list-versions
.PHONY : config
.PHONY : build
.PHONY : test
.PHONY : test-one check-test-one
.PHONY : check-git-version check-subdaemon
