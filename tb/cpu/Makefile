SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs -Wno-WIDTHTRUNC
WAVES = 1

TOPLEVEL = cpu
VERILOG_SOURCES += $(PWD)/../../src/pkg.sv
VERILOG_SOURCES += $(PWD)/../../src/$(TOPLEVEL).sv
VERILOG_SOURCES += $(PWD)/../../src/alu.sv
VERILOG_SOURCES += $(PWD)/../../src/control.sv
VERILOG_SOURCES += $(PWD)/../../src/program_counter.sv
VERILOG_SOURCES += $(PWD)/../../src/instruction_memory.sv
VERILOG_SOURCES += $(PWD)/../../src/regfile.sv
VERILOG_SOURCES += $(PWD)/../../src/sign_extender.sv
VERILOG_SOURCES += $(PWD)/../../src/data_memory.sv

# MODULE is the basename of the Python test file
MODULE = tb_$(TOPLEVEL)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
