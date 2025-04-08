from decimal import Decimal
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def bin_to_hex(bin) -> str:
    return hex(int(str(bin), 2)).upper()


def read_hex_file(file: Path) -> list[int]:
    hex = []
    with file.open("r") as f:
        content = f.readlines()
        for line in content:
            hex.append(int(line.split("//")[0].strip().upper(), base=16))
    return hex


@cocotb.coroutine
async def cpu_reset(dut):
    dut.reset_n.value = 0
    await RisingEdge(dut.clk)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)


@cocotb.test
async def test_cpu_init(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await cpu_reset(dut)

    assert dut.pc.value == 0

    instruction_memory = read_hex_file(Path("./instruction_memory.hex"))

    # Check that instruction are still in memory
    for i in range(len(instruction_memory)):
        assert dut.instr_mem.memory[i].value == instruction_memory[i]

    # Test that instruction given by PC during executions are the ones expected
    # Only test for a few instructions, branching occurs after the start of the program
    maximum_instruction_to_test = 4
    for i in range(min(maximum_instruction_to_test, len(instruction_memory))):
        expected_instruction = instruction_memory[i]
        assert dut.instruction.value == expected_instruction
        await RisingEdge(dut.clk)

@cocotb.test
async def test_instructions(dut):
    print("data_mem.addr: ", bin_to_hex(dut.alu_result.value))
    dut._log.info(f"data_mem: {dut.data_mem.memory.value[:4]}")
    print("data_memory_value: ", bin_to_hex(dut.data_memory_value.value))
    await Timer(Decimal(1), units="ns")
    dut._log.info(f"data_mem: {dut.instr_mem.memory.value[:4]}")
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # imem contains:
    # LW x5, 12(x0)
    imem = read_hex_file(Path("./instruction_memory.hex"))
    assert dut.instruction.value == imem[0]
    assert dut.pc_next.value == 0x4
    assert dut.imm_ext.value == 12
    assert dut.read_data_registers1.value == 0
    print("data_mem.addr: ", bin_to_hex(dut.alu_result.value))
    print("data_mem.value: ", bin_to_hex(dut.data_memory_value.value))
    await RisingEdge(dut.clk)
    print("data_mem: ", bin_to_hex(dut.data_memory_value.value))
