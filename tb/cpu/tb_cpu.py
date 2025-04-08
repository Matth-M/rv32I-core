from decimal import Decimal
from pathlib import Path

import cocotb
from cocotb.triggers import Timer

def bin_to_hex(bin) -> str:
    return hex(int(str(bin), 2)).upper()


def read_hex_file(file: Path) -> list[int]:
    hex = []
    with file.open("r") as f:
        content = f.readlines()
        for line in content:
            hex.append(int(line.split("//")[0].strip().upper(), base=16))
    return hex


@cocotb.test
async def test(dut):
    await Timer(Decimal(1),units="ns")
    dut._log.info(f"instruction_memory: {dut.instr_mem.memory.value[0]}")
