import cocotb
from cocotb.triggers import Timer
from decimal import Decimal

@cocotb.test
async def test(dut):
    # lw x6, -4(x9)
    dut.instruction.value = 0xFFC4A303
    dut.imm_src.value = 0
    await Timer(Decimal(1), units="ns")
    dut._log.info(f"instruction: {hex(dut.instruction.value)}")
    dut._log.info(f"imm_ext: {hex(dut.imm_ext.value)}")
    assert dut.imm_ext.value == 0xFFFFFFFC, f"{hex(int(str(dut.imm_ext.value),2))}"

    # sw x6, 8(x9)
    dut.instruction.value = 0x0064A423
    dut.imm_src = 1
    await Timer(Decimal(1), units="ns")
    dut._log.info(f"instruction: {hex(dut.instruction.value)}")
    dut._log.info(f"imm_ext: {hex(dut.imm_ext.value)}")
    assert dut.imm_ext.value == 0x00000008, f"{hex(int(str(dut.imm_ext.value),2))}"
