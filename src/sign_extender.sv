`default_nettype none
module sign_extender (
    input  wire [ 1:0] imm_src,
    input  wire [31:0] instruction,
    output wire [31:0] imm_ext
);

  always_comb begin
    case (imm_src)
      IMM_SRC_I_TYPE: imm_ext = {{20{instruction[31]}}, instruction[31:20]};
      IMM_SRC_S_TYPE: imm_ext = {{20{instruction[31]}}, instruction[31:25], instruction[11:7]};
      default: imm_ext = 32'b0;
    endcase
  end
endmodule
