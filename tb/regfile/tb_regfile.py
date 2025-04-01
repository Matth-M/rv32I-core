import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test
async def test(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Register 0 holds always value 0
    dut.write_address.value = 0
    dut.write_data.value = 0xFFC4A303
    await RisingEdge(dut.clk)
    dut.read_address1.value = 0
    await Timer(1, units="ns")
    assert dut.read_data1.value == 0

    for _ in range(100):
        dut.reset_n.value = 1
        write_address = random.randint(1, 2**5 - 1)
        write_data = random.randint(0, 2**32 - 1)
        dut.write_enable.value = 1
        dut.write_address.value = write_address
        dut.write_data.value = write_data
        dut.read_address1.value = write_address
        await Timer(1, units="ns")
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.read_data1.value == write_data


        # Don't write with write enable unset
        dut.write_enable.value = 0
        new_value_no_override = random.randint(0, 2**32 - 1)
        dut.write_data.value = new_value_no_override
        await Timer(1, units="ns")
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.read_data1.value == write_data


        # Reset
        dut.reset_n.value = 0
        await Timer(1, units="ns")
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.read_data1.value == 0

