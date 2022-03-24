
JPAR:=$(shell nproc)
TPAR:=$$(( $(JPAR) * 2 ))

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
	touch $@

.config-standard .config-experimental:
	rm -f .config-standard .config-experimental
	cd lightning \
		&& make distclean && ./configure --enable-developer $(CFGFLAGS)
	touch $@

build build-standard build-experimental:
	cd vls && cargo build
	cd greenlight-signer && cargo build
	cd lightning && make -j$(JPAR)

test-standard test-experimental:
	-source scripts/setup-env && cd lightning \
		&& make -j$(JPAR) PYTEST_PAR=$(TPAR) DEVELOPER=1 VALGRIND=0 pytest \
		|& tee ../$(LOGFILE)

clean:
	rm -f .config-standard .config-experimental
	cd vls && cargo clean
	cd lightning && make distclean

test-one:	check-test-one build
	source scripts/setup-env && cd lightning \
		&& ../scripts/run-one-test $(test)

check-test-one:
	@if test -z $(test); then echo "usage: make test-one test=<your-test-here>"; exit 1; fi
