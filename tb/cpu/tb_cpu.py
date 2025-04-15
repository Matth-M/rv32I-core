import os
import sys
from decimal import Decimal
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cocotb
import utils
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


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

    instruction_memory = utils.read_hex_file(Path("./instruction_memory.hex"))

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

    # Expected values of registers, imem and dmem
    expected_registers = [0] * len(dut.regfile.registers)
    expected_dmem = [0] * len(dut.dmem.memory)

    ##############
    # LW x5, 12(x0)
    # M[12] == 0xDEADBEEF
    ##############
    print("LW TEST")
    expected_registers[5] = 0xDEADBEEF

    # Wait for execution of the instruction, one clock cycle to write to register
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[5].value == expected_registers[5]

    ##############
    # SW x5, 8(x0)
    # r5 == 0xDEADBEEF
    ##############
    print("SW TEST")
    expected_dmem[2] = 0xDEADBEEF
    await RisingEdge(dut.clk)
    # 8th bytes -> 3rd word
    assert dut.dmem.memory[2].value == expected_dmem[2]

    ##############
    # ADD x28, x5, x5
    ##############
    print("ADD TEST")
    expected_registers[28] = utils.truncate_32_bits(
        expected_registers[5] + expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[28].value == expected_registers[28]

    ##############
    # SUB x29, x5, x28
    ##############
    print("SUB TEST")
    expected_registers[29] = utils.truncate_32_bits(
        expected_registers[5] - expected_registers[28]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[29].value == expected_registers[29]

    ##############
    # XOR x30, x28, x29
    ##############
    print("XOR TEST")
    expected_registers[30] = utils.truncate_32_bits(
        expected_registers[28] ^ expected_registers[29]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[30].value == expected_registers[30]

    ##############
    # OR x31, x30, x5
    ##############
    print("OR TEST")
    expected_registers[31] = utils.truncate_32_bits(
        expected_registers[30] | expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[31].value == expected_registers[31]

    ##############
    # AND x6, x30, x5
    ##############
    print("AND TEST")
    expected_registers[6] = utils.truncate_32_bits(
        expected_registers[30] & expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[6].value == expected_registers[6]

    ##############
    # SLL x7, x6, x5
    ##############
    print("SLL TEST")
    expected_registers[7] = utils.truncate_32_bits(
        expected_registers[6] << expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[7].value == expected_registers[7]

    ##############
    # SRL x28, x7, x6
    ##############
    print("SRL TEST")
    expected_registers[28] = utils.truncate_32_bits(
        expected_registers[7] >> expected_registers[6]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[7].value == expected_registers[7]

    ##############
    # SRA x7, x6, x5
    ##############
    print("SRA TEST")
    expected_registers[7] = utils.truncate_32_bits(
        expected_registers[6] >> expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[7].value == expected_registers[7]

    ##############
    # SLT x7, x6, x5
    ##############
    print("SLT TEST")
    expected_registers[7] = utils.truncate_32_bits(
        expected_registers[6] < expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[7].value == expected_registers[7]

    ##############
    # SLTU x7, x6, x5
    ##############
    print("SLTU TEST")
    expected_registers[7] = utils.truncate_32_bits(
        expected_registers[6] < expected_registers[5]
    )
    await RisingEdge(dut.clk)
    assert dut.regfile.registers[7].value == expected_registers[7]
