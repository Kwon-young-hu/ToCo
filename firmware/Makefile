
SYS_ROOT = /home/kwan/cortdev/g3-eng.sdk.r1.1.6.0/build/tmp/work/aarch64-poky-linux
UCI_ROOT = $(SYS_ROOT)/uci/1.0-r0/package
UCI_CFLAGS="-I$(UCI_ROOT)/usr/include"
UCI_LDFLAGS="-L$(UCI_ROOT)/usr/lib/"
CFLAGS += $(UCI_CFLAGS)
LDFLAGS += $(UCI_LDFLAGS)

UBOX_ROOT = $(SYS_ROOT)/libubox/git-r0/package
UBOX_LDFLAGS="-L$(UBOX_ROOT)/usr/lib/"
LDFLAGS += $(UBOX_LDFLAGS)

LIB_NAME = uci_conf
LIB_LDNAME = lib$(LIB_NAME).so
LIB_SONAME = $(LIB_LDNAME).1
LIB_REALNAME = $(LIB_LDNAME).1.0.1


LIBS += -luci

SAMPLE_OBJS = fw_upgrade.o

TARGETS = fw_upgrade

all: $(TARGETS)

-include $(shell find . -name \*.d)


fw_upgrade: ${SAMPLE_OBJS:%=build/%}
	${CC} $(filter %.o, $^) $(LDFLAGS) -L. -l$(LIB_NAME) -luci -lubox -o $@

build/%.o: %.c
	@mkdir -p ${@D}
	${CC} ${CFLAGS} -I. $< -c -o $@ -MD -MF $@.d

clean:
	rm -rf build $(TARGETS)
