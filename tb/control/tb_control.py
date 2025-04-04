from decimal import Decimal

import cocotb
from cocotb.triggers import Timer


@cocotb.test
async def test_I_type(dut):
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
    assert dut.alu_op.value == 0
