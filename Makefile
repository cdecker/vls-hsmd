
JPAR:=$(shell nproc)
TPAR:=$$(( $(JPAR) * 2 ))

.PHONY : all test-all setup clean
.PHONY : config-standard config-experimental
.PHONY : build-standard build-experimental
.PHONY : test-standard test-experimental

all: test-standard

test-all: test-standard test-experimental

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

build-standard build-experimental:
	cd vls && cargo build
	cd lightning && make -j$(JPAR)

test-standard test-experimental:
	-source scripts/setup-env && cd lightning \
		&& make -j$(JPAR) PYTEST_PAR=$(TPAR) DEVELOPER=1 VALGRIND=0 pytest \
		|& tee ../$(LOGFILE)

clean:
	rm -f .config-standard .config-experimental
	cd vls && cargo clean
	cd lightning && make distclean
