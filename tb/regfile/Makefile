SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1

TOPLEVEL = regfile
VERILOG_SOURCES += $(PWD)/../../src/$(TOPLEVEL).sv

# MODULE is the basename of the Python test file
MODULE = tb_$(TOPLEVEL)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
