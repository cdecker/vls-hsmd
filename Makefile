
JPAR:=$(shell nproc)
TPAR:=$$(( $(JPAR) * 2 ))


ifeq ($(GREENLIGHT_VLS),)
	SUBDAEMON:="hsmd:remote_hsmd"
else
	SUBDAEMON:="hsmd:remote_hsmd_vls"
endif

GITDESC:=$(shell git describe --tags --long --always --match='v*.*')

.PHONY : all test-all setup clean summary
.PHONY : config-standard config-experimental
.PHONY : build build-standard build-experimental
.PHONY : test-standard test-experimental
.PHONY : test-one check-test-one

all: test-standard

test-all: test-standard test-experimental summary

summary:
	./scripts/summary standard.log
	./scripts/summary experimental.log

setup:	.setup-complete
ifneq ($(GITDESC),$(shell cat .setup-complete))
	@echo "git hash changed, rerunning setup"
	rm .setup-complete
	make .setup-complete
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

.setup-complete:
	git submodule update --init
	./scripts/setup-remote-hsmd
	mkdir -p $(PWD)/bin
	(cd bin && ln -fs ../vls/target/debug/vlsd)
	(cd bin && ln -fs ../greenlight-signer/target/debug/remote_hsmd_vls)
	echo "$(GITDESC)" > $@

.config-standard .config-experimental:
	rm -f .config-standard .config-experimental
	cd lightning \
		&& make distclean && ./configure --enable-developer $(CFGFLAGS)
	touch $@

build build-standard build-experimental:	setup
	cd vls && cargo build
	cd greenlight-signer && cargo build
	cd lightning && make -j$(JPAR)

test-standard test-experimental:
	-. scripts/setup-env && cd lightning \
		&& SUBDAEMON=$(SUBDAEMON) \
		make -j$(JPAR) PYTEST_PAR=$(TPAR) DEVELOPER=1 VALGRIND=0 pytest \
		| tee ../$(LOGFILE) 2>&1

clean:
	rm -f .config-standard .config-experimental
	cd vls && cargo clean
	cd lightning && make distclean

test-one:	LOGFILE = one.log
test-one:	check-configured check-test-one build
	. scripts/setup-env && cd lightning \
		&& SUBDAEMON=$(SUBDAEMON) ../scripts/run-one-test $(test) \
		| tee ../$(LOGFILE) 2>&1

check-test-one:
	@if test -z $(test); then echo "usage: make test-one test=<your-test-here>"; exit 1; fi

check-configured:
ifeq (,$(wildcard ./.config-*))
	@echo "You must choose a configuration with \"make config-standard\" or \"make config-experimental\" first"
	exit 1
endif
