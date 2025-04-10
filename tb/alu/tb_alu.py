import os
import sys
from decimal import Decimal
import random

import cocotb
from cocotb.triggers import Timer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# ALU control signals
ALU_ADD = 0b0000
ALU_SUB = 0b0001
ALU_XOR = 0b0010
ALU_OR = 0b0011
ALU_AND = 0b0100
ALU_SLL = 0b0101
ALU_SRL = 0b0110
ALU_SRA = 0b0111
ALU_SLT = 0b1000
ALU_SLTU = 0b1001


@cocotb.test
async def test(dut):
    for _ in range(20):
        a = random.randint(0, 0xFFFFFFFF)
        b = random.randint(0, 0xFFFFFFFF)
        sum = utils.truncate_32_bits(a + b)
        diff = utils.truncate_32_bits(a - b)
        xor = utils.truncate_32_bits(a ^ b)
        result_or = utils.truncate_32_bits(a | b)
        result_and = utils.truncate_32_bits(a & b)
        sll = utils.truncate_32_bits(a << b)
        srl = utils.truncate_32_bits(a >> b)
        sra = utils.truncate_32_bits(a >> b)
        slt = utils.truncate_32_bits(a < b)
        sltu = utils.truncate_32_bits(a < b)

        dut.srcA.value = a
        dut.srcB.value = b
        # ADD
        dut.alu_control.value = ALU_ADD
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == sum

        # SUB
        dut.alu_control.value = ALU_SUB
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == diff

        # XOR
        dut.alu_control.value = ALU_XOR
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == xor

        # OR
        dut.alu_control.value = ALU_OR
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == result_or

        # AND
        dut.alu_control.value = ALU_AND
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == result_and

        # SLL
        dut.alu_control.value = ALU_SLL
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == sll

        # SRL
        dut.alu_control.value = ALU_SRL
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == srl

        # SRA
        dut.alu_control.value = ALU_SRA
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == sra

        # SLT
        dut.alu_control.value = ALU_SLT
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == slt

        # SLTU
        dut.alu_control.value = ALU_SLTU
        await Timer(Decimal(1), units="ns")
        assert dut.result.value == sltu
