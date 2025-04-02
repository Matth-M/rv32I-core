from decimal import Decimal

import cocotb
from cocotb.triggers import Timer


@cocotb.test
async def test(dut):
    # ADD
    dut.srcA.value = 0x2004
    dut.srcB.value = 0xFFFFFFFC
    dut.alu_control.value = int("010", 2)
    await Timer(Decimal(1), units="ns")
    assert dut.result.value == 0x2000
