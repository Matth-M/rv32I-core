from decimal import Decimal

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test
async def test(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await RisingEdge(dut.clk)
    # Reset
    dut.reset_n.value = 0
    dut.write_enable.value = 0
    await RisingEdge(dut.clk)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)

    data = [
        (0, 0x12345678),
        (4, 0xABCDEF12),
        (8, 0x98765432),
        (12, 0xABABABAB),
    ]

    dut.write_enable.value = 0
    for addr, d in data:
        # Attempting to write without write enable set should fail
        dut.address.value = addr
        dut.write_data.value = d
        await RisingEdge(dut.clk)
        await Timer(Decimal(1), units="ns")
        assert dut.data.value == 0

    dut.write_enable.value = 1
    for addr, d in data:
        dut.address.value = addr
        dut.write_data.value = d
        await Timer(Decimal(1), units="ns")
        assert dut.write_data.value == d
