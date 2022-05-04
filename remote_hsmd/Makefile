#! /usr/bin/make

RMTHSMD_SRC := contrib/remote_hsmd/hsmd.c	\
	contrib/remote_hsmd/remotesigner.pb.cc \
	contrib/remote_hsmd/remotesigner.grpc.pb.cc \
	contrib/remote_hsmd/dump.cc \
	contrib/remote_hsmd/proxy.cc

RMTHSMD_HEADERS := contrib/remote_hsmd/remotesigner.pb.h \
	contrib/remote_hsmd/remotesigner.grpc.pb.h
RMTHSMD_CCOBJS := $(RMTHSMD_SRC:.cc=.o)
RMTHSMD_OBJS := $(RMTHSMD_CCOBJS:.c=.o)

$(RMTHSMD_OBJS): $(RMTHSMD_HEADERS)

# Make sure these depend on everything.
ALL_PROGRAMS += lightningd/remote_hsmd

# Common source we use.
RMTHSMD_COMMON_OBJS :=				\
    hsmd/hsmd_wiregen.o			\
	common/amount.o				\
	common/autodata.o			\
	common/base32.o				\
	common/bigsize.o			\
	common/bip32.o				\
	common/channel_id.o			\
	common/channel_type.o		\
	common/daemon.o				\
	common/daemon_conn.o			\
	common/derive_basepoints.o		\
	common/features.o			\
	common/status_wire.o		\
	common/status_wiregen.o		\
	common/hash_u5.o			\
	common/htlc_state.o			\
	common/htlc_wire.o			\
	common/key_derive.o			\
	common/memleak.o			\
	common/msg_queue.o			\
	common/node_id.o			\
	common/onionreply.o			\
	common/permute_tx.o			\
	common/pseudorand.o			\
	common/setup.o				\
	common/status.o				\
	common/status_wire.o		\
	common/status_wiregen.o		\
	common/subdaemon.o			\
	common/type_to_string.o		\
	common/utils.o				\
	common/utxo.o				\
	common/version.o			\
	common/wireaddr.o

CXX = g++
CXXFLAGS += -std=c++11 \
	-I. \
	-Iccan \
	-Iexternal/libwally-core/include \
	-Iexternal/libwally-core/src/secp256k1/include \
	-g
PROTOC = protoc
GRPC_CPP_PLUGIN = grpc_cpp_plugin
GRPC_CPP_PLUGIN_PATH ?= `which $(GRPC_CPP_PLUGIN)`
PROTOS_PATH = contrib/remote_hsmd

lightningd/remote_hsmd: $(RMTHSMD_OBJS) $(LIGHTNINGD_LIB_OBJS) $(RMTHSMD_COMMON_OBJS) $(BITCOIN_OBJS) $(WIRE_OBJS)

clean: rmthsmd-clean

rmthsmd-clean:
	$(RM) $(RMTHSMD_OBJS)
	$(RM) contrib/remote_hsmd/*.pb.cc contrib/remote_hsmd/*.pb.h

GEN_HEADERS += contrib/remote_hsmd/remotesigner.pb.h \
	contrib/remote_hsmd/remotesigner.grpc.pb.h

contrib/remote_hsmd/remotesigner.pb.o: $(GEN_HEADERS)

contrib/remote_hsmd/dump.o contrib/remote_hsmd/proxy.o: $(GEN_HEADERS)

contrib/remote_hsmd/remotesigner.grpc.pb.o contrib/remote_hsmd/remotesigner.pb.o contrib/remote_hsmd/proxy.o contrib/remote_hsmd/dump.o : CPPFLAGS +=  $(CMNFLAGS) `pkg-config --cflags protobuf grpc`
lightningd/remote_hsmd: LDLIBS += -L/usr/local/lib \
	`pkg-config --libs protobuf grpc++`\
	-pthread\
	-Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed\
	-ldl
lightningd/remote_hsmd: LDLIBS += -lstdc++

.PRECIOUS: %.grpc.pb.cc
%.grpc.pb.cc: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --grpc_out=contrib/remote_hsmd --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) $<

.PRECIOUS: %.pb.cc
%.pb.cc: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --cpp_out=contrib/remote_hsmd $<

.PRECIOUS: %.grpc.pb.h
%.grpc.pb.h: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --grpc_out=contrib/remote_hsmd --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) $<

.PRECIOUS: %.pb.h
%.pb.h: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --cpp_out=contrib/remote_hsmd $<

-include contrib/remote_hsmd/test/Makefile
