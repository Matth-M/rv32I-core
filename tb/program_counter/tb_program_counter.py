import random

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

    address = 0x04
    dut.pc_next.value = address
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.pc.value == address

    await RisingEdge(dut.clk)
    dut.reset_n.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.pc.value == 0
