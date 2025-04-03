from decimal import Decimal

import cocotb
from cocotb.triggers import Timer


@cocotb.test
async def test(dut):
    await Timer(Decimal(1),units="ns")
    dut._log.info(f"instruction_memory: {dut.instr_mem.memory.value[0]}")
