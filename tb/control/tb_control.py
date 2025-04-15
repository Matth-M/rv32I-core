from decimal import Decimal

import cocotb
from cocotb.triggers import Timer

ALU_ADD = 0b0000
ALU_SUB = 0b0001
ALU_XOR = 0b0010
ALU_OR = 0b0011
ALU_AND = 0b0100
ALU_SLL = 0b0101
ALU_SRL = 0b0110
ALU_SRA = 0b0111
ALU_SLT = 0b1000
ALU_SLTU = 0b1001


@cocotb.test
async def test_I_LOAD(dut):
    # LW
    opcode = int("0000011", 2)
    funct3 = 0x2
    dut.opcode.value = opcode
    dut.funct3.value = funct3
    await Timer(Decimal(1), units="ns")
    assert dut.reg_write_enable.value == 1
    assert dut.imm_src.value == 0
    assert dut.alu_src.value == 1
    assert dut.data_mem_write_enable.value == 0
    assert dut.result_src.value == 1
    assert dut.branch.value == 0
    assert dut.alu_control.value == ALU_ADD


@cocotb.test
async def test_S_type(dut):
    # SW
    opcode = int("0100011", 2)
    funct3 = 0x2
    dut.opcode.value = opcode
    dut.funct3.value = funct3
    await Timer(Decimal(1), units="ns")
    assert dut.reg_write_enable.value == 0
    assert dut.imm_src.value == 1
    assert dut.alu_src.value == 1
    assert dut.data_mem_write_enable.value == 1
    assert dut.branch.value == 0
    assert dut.alu_control.value == ALU_ADD


@cocotb.test
async def test_R_type(dut):
    rtype_opcode = 0b0110011
    dut.opcode.value = rtype_opcode
    rtypes = {
        "ADD": {"funct3": 0x0, "funct7": 0x00, "expected_alu_control": ALU_ADD},
        "SUB": {"funct3": 0x0, "funct7": 0x20, "expected_alu_control": ALU_SUB},
        "XOR": {"funct3": 0x4, "funct7": 0x00, "expected_alu_control": ALU_XOR},
        "OR": {"funct3": 0x6, "funct7": 0x00, "expected_alu_control": ALU_OR},
        "AND": {"funct3": 0x7, "funct7": 0x00, "expected_alu_control": ALU_AND},
        "SLL": {"funct3": 0x1, "funct7": 0x00, "expected_alu_control": ALU_SLL},
        "SRL": {"funct3": 0x5, "funct7": 0x00, "expected_alu_control": ALU_SRL},
        "SRA": {"funct3": 0x5, "funct7": 0x20, "expected_alu_control": ALU_SRA},
        "SLT": {"funct3": 0x2, "funct7": 0x00, "expected_alu_control": ALU_SLT},
        "SLTU": {"funct3": 0x3, "funct7": 0x00, "expected_alu_control": ALU_SLTU},
    }
    for instruction in rtypes.values():
        dut.funct3.value = instruction["funct3"]
        dut.funct7.value = instruction["funct7"]
        await Timer(Decimal(1), units="ns")
        assert dut.reg_write_enable.value == 1
        assert dut.alu_src.value == 0
        assert dut.data_mem_write_enable.value == 0
        assert dut.branch.value == 0
        assert dut.alu_control.value == instruction["expected_alu_control"]


@cocotb.test
async def test_I_MATH_type(dut):
    rtype_opcode = 0b0110011
    dut.opcode.value = rtype_opcode
    rtypes = {
        "ADDI": {"funct3": 0x0, "funct7": 0x00, "expected_alu_control": ALU_ADD},
        "XORI": {"funct3": 0x4, "funct7": 0x00, "expected_alu_control": ALU_XOR},
        "ORI": {"funct3": 0x6, "funct7": 0x00, "expected_alu_control": ALU_OR},
        "ANDI": {"funct3": 0x7, "funct7": 0x00, "expected_alu_control": ALU_AND},
        "SLLI": {"funct3": 0x1, "funct7": 0x00, "expected_alu_control": ALU_SLL},
        "SRLI": {"funct3": 0x5, "funct7": 0x00, "expected_alu_control": ALU_SRL},
        "SRAI": {"funct3": 0x5, "funct7": 0x20, "expected_alu_control": ALU_SRA},
        "SLTI": {"funct3": 0x2, "funct7": 0x00, "expected_alu_control": ALU_SLT},
        "SLTIU": {"funct3": 0x3, "funct7": 0x00, "expected_alu_control": ALU_SLTU},
    }
    for instruction in rtypes.values():
        dut.funct3.value = instruction["funct3"]
        dut.funct7.value = instruction["funct7"]
        await Timer(Decimal(1), units="ns")
        assert dut.reg_write_enable.value == 1
        assert dut.alu_src.value == 0
        assert dut.data_mem_write_enable.value == 0
        assert dut.branch.value == 0
        assert dut.alu_control.value == instruction["expected_alu_control"]
