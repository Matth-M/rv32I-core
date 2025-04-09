from decimal import Decimal
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def bin_to_hex(bin) -> str:
    return hex(int(str(bin), 2)).upper().split("X")[1].zfill(8)


def read_hex_file(file: Path) -> list[int]:
    hex = []
    with file.open("r") as f:
        content = f.readlines()
        for line in content:
            hex.append(int(line.split("//")[0].strip().upper(), base=16))
    return hex


def bin_array_to_hex(bin_array: list) -> list:
    return list(map(bin_to_hex, bin_array))


@cocotb.coroutine
async def cpu_reset(dut):
    dut.reset_n.value = 0
    await RisingEdge(dut.clk)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)


@cocotb.test
async def test_cpu_init(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await Timer(Decimal(1), units="ns")
    await cpu_reset(dut)

    assert dut.pc.value == 0

    instruction_memory = read_hex_file(Path("./instruction_memory.hex"))

    # Check that instruction are still in memory
    for i in range(len(instruction_memory)):
        assert dut.imem.memory[i].value == instruction_memory[i]

    # Test that instruction given by PC during executions are the ones expected
    # Only test for a few instructions, branching occurs after the start of the program
    maximum_instruction_to_test = 4
    for i in range(min(maximum_instruction_to_test, len(instruction_memory))):
        expected_instruction = instruction_memory[i]
        assert dut.instruction.value == expected_instruction
        await RisingEdge(dut.clk)


@cocotb.test
async def test_instructions(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await cpu_reset(dut)

    ##############
    # LW x5, 12(x0)
    # M[12] == 0xDEADBEEF
    ##############
    print("\n\nLW TEST\n\n")

    # Wait for execution of the instruction, one clock cycle to write to register
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[5].value == 0xDEADBEEF
