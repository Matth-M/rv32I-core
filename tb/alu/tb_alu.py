from decimal import Decimal

import cocotb
from cocotb.triggers import Timer

# ALU control signals
ALU_ADD = 0b0000
ALU_SUB = 0b0001
ALU_XOR = 0b0010
ALU_OR  = 0b0011
ALU_AND = 0b0100
ALU_SLL = 0b0101
ALU_SRL = 0b0110
ALU_SRA = 0b0111
ALU_SLT = 0b1000
ALU_SLTU = 0b1001

@cocotb.test
async def test(dut):
    # ADD
    dut.srcA.value = 0x2004
    dut.srcB.value = 0xFFFFFFFC
    dut.alu_control.value = int("010", 2)
    await Timer(Decimal(1), units="ns")
    assert dut.result.value == 0x2000
