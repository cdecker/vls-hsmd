
VALGRIND ?= 0

JPAR:=$(shell nproc)
TPAR:=$$(( $(JPAR) * 2 ))

VLS_MODE ?= cln:standalone

ifeq ("$(VLS_MODE)","cln:standalone")
	SUBDAEMON:="hsmd:remote_hsmd"
else ifeq ("$(VLS_MODE)","cln:inplace")
	SUBDAEMON:="hsmd:remote_hsmd_vls"
else ifeq ("$(VLS_MODE)","cln:socket")
	SUBDAEMON:="hsmd:remote_hsmd_vls_grpc2"
else ifeq ("$(VLS_MODE)","cln:native")
	SUBDAEMON:="hsmd:lightning_hsmd"
else ifeq ("$(VLS_MODE)","cln:embedded")
    # embedded for node 1, native for the rest
	SUBDAEMON:="hsmd:remote_hsmd_vls_embedded,hsmd:lightning_hsmd"
endif

GITDESC:=$(shell git describe --tags --long --always --match='v*.*')

all: test-standard

test-all: test-standard test-experimental summary

summary:
	./scripts/summary standard.log
	./scripts/summary experimental.log

setup:	check-git-version .setup-complete

check-git-version:
ifneq ("$(wildcard .setup-complete)", "")
  ifneq ($(GITDESC),$(shell cat .setup-complete))
	@echo "git hash changed, rerunning setup"
	rm .setup-complete
  endif
endif

config-standard:	setup .config-standard
config-standard:	CFGFLAGS=

config-experimental:	setup .config-experimental
config-experimental:	CFGFLAGS = --enable-experimental-features

build-standard:		config-standard
build-experimental:		config-experimental

test-standard:	build-standard
test-standard:	LOGFILE = standard.log

test-experimental:	build-experimental
test-experimental:	LOGFILE = experimental.log

.setup-complete: ./scripts/setup-remote-hsmd
	git submodule update --init --recursive
	./scripts/enable-githooks
	./scripts/setup-remote-hsmd
	mkdir -p $(PWD)/bin
	(cd bin && ln -fs ../vls/target/debug/vlsd)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_vls)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_vls_grpc2)
	(cd bin && ln -fs ../vls/target/debug/remote_hsmd_vls_embedded)
	echo "$(GITDESC)" > $@

.config-standard .config-experimental:
	rm -f .config-standard .config-experimental
	cd lightning \
		&& make distclean \
		&& poetry install \
		&& ./configure --enable-developer $(CFGFLAGS)
	touch $@

build build-standard build-experimental:	setup
	cd vls && cargo build
	cd lightning && make -j$(JPAR)

test-standard test-experimental:	check-subdaemon
	-. scripts/setup-env && cd lightning \
		&& SUBDAEMON=$(SUBDAEMON) \
		poetry run make -j$(JPAR) PYTEST_PAR=$(TPAR) DEVELOPER=1 VALGRIND=$(VALGRIND) pytest \
		| tee ../$(LOGFILE) 2>&1

clean:
	rm -f .config-standard .config-experimental
	cd vls && cargo clean
	cd lightning && make distclean

test-one:	LOGFILE = one.log
test-one:	check-configured check-subdaemon check-test-one build
	. scripts/setup-env && cd lightning \
		&& SUBDAEMON=$(SUBDAEMON) VALGRIND=$(VALGRIND) poetry run ../scripts/run-one-test $(test) \
		| tee ../$(LOGFILE) 2>&1

check-subdaemon:
	@if test -z $(SUBDAEMON); then echo "unknown VLS_MODE $(VLS_MODE)"; exit 1; fi

check-test-one:
	@if test -z $(test); then echo "usage: make test-one test=<your-test-here>"; exit 1; fi

check-configured:
	@if test ! -e .config-standard && test ! -e .config-experimental; then \
		echo "Need \"make config-standard\" or \"make config-experimental\" first"; exit 1; fi

.PHONY : all test-all setup clean summary
.PHONY : config-standard config-experimental
.PHONY : build build-standard build-experimental
.PHONY : test-standard test-experimental
.PHONY : test-one check-test-one
.PHONY : check-git-version check-configured check-subdaemon

