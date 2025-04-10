`default_nettype none
import pkg::*;
module alu (
    input logic [31:0] srcA,
    input logic [31:0] srcB,
    input logic [3:0] alu_control,
    output logic zero,
    output logic [31:0] result
);

  always_comb begin
    case (alu_control)
      ALU_ADD:  result = srcA + srcB;
      ALU_SUB:  result = srcA - srcB;
      ALU_XOR:  result = srcA ^ srcB;
      ALU_OR:   result = srcA | srcB;
      ALU_AND:  result = srcA & srcB;
      ALU_SLL:  result = srcA << srcB;
      ALU_SRL:  result = srcA >> srcB;
      ALU_SRA:  result = srcA >>> srcB;
      ALU_SLT:  result = srcA < srcB ? 1 : 0;
      ALU_SLTU: result = {{31{1'b0}}, (srcA < srcB ? 1'b1 : 1'b0)};

      default: result = 32'b0;
    endcase
  end

  assign zero = result == 32'b0;
endmodule
