import random
from decimal import Decimal

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test
async def test(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await RisingEdge(dut.clk)
    dut.reset_n.value = 0
    await RisingEdge(dut.clk)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)

    for _ in range(100):
        address = random.randint(0, 64)
        dut.read_address = address
        await Timer(Decimal(1), units="ns")
        assert dut.instruction == 0
