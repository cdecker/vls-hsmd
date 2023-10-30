
VLS_MODE ?= cln:socket
TIMEOUT ?= 120
VALGRIND ?= 0

JPAR:=$(shell nproc)
# TPAR:=$$(( $(JPAR) * 2 ))
TPAR=$(JPAR)

ifeq ("$(VLS_MODE)","cln:inplace")
	SUBDAEMON:="hsmd:remote_hsmd_inplace"
else ifeq ("$(VLS_MODE)","cln:socket")
	SUBDAEMON:="hsmd:remote_hsmd_socket"
else ifeq ("$(VLS_MODE)","cln:native")
	SUBDAEMON:="hsmd:lightning_hsmd"
else ifeq ("$(VLS_MODE)","cln:serial")
    # embedded for node 1, native for the rest
	SUBDAEMON:="hsmd:remote_hsmd_serial,hsmd:lightning_hsmd"
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
test:	LOGFILE = all.log

.setup-complete: ./scripts/setup-remote-hsmd
	git submodule update --init --recursive
	./scripts/enable-githooks
	./scripts/setup-remote-hsmd
	mkdir -p $(PWD)/bin
	(cd bin && ln -fs ../vls/target/debug/vlsd2)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_inplace)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_socket)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_serial)
	(cd bin && ln -fs ../vls/lightning-storage-server/target/debug/lssd)
	echo "$(GITDESC)" > $@

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
	cd vls && cargo build --bins $(VLS_BUILDARGS)
	cd vls/lightning-storage-server && cargo build --bins $(LSS_BUILDARGS)

test:	check-subdaemon
	-. scripts/setup-env && cd lightning \
		&& SUBDAEMON=$(SUBDAEMON) \
		poetry run make -j$(JPAR) \
			PYTEST_PAR=$(TPAR) \
			DEVELOPER=1 \
			VALGRIND=$(VALGRIND) \
			TIMEOUT=$(TIMEOUT) \
		pytest \
		2>&1 | tee ../$(LOGFILE)

clean:
	rm -f .config
	cd vls && cargo clean
	cd lightning && make distclean

test-one:	LOGFILE = one.log
test-one:	check-subdaemon check-test-one build
	. scripts/setup-env && cd lightning \
		&& SUBDAEMON=$(SUBDAEMON) VALGRIND=$(VALGRIND) poetry run ../scripts/run-one-test $(TEST) \
		2>&1 | tee ../$(LOGFILE)

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

