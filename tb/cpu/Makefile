SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs -Wno-WIDTHTRUNC
WAVES = 1

TOPLEVEL = cpu
VERILOG_SOURCES += $(PWD)/../../src/pkg.sv
VERILOG_SOURCES+=$(shell find ../../src -name "*.sv" -not -name "pkg.sv")


# MODULE is the basename of the Python test file
MODULE = tb_$(TOPLEVEL)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
