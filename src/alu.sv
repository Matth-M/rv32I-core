`default_nettype none
import pkg::*;
module alu (
    input logic [31:0] srcA,
    input logic [31:0] srcB,
    input logic [2:0] alu_control,
    output logic zero,
    output logic [31:0] result
);

  always_comb begin
    case (alu_control)
      ALU_ADD: result = srcA + srcB;
      default: result = 32'b0;
    endcase
  end

  assign zero = result == 32'b0;
endmodule
