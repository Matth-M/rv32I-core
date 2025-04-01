`default_nettype none
module sign_extender (
    input wire imm_src,
    input wire [31:0] instruction,
    output wire [31:0] imm_ext
);
  assign imm_ext = imm_src ?
	  {{20{instruction[31]}}, instruction[31:25], instruction[11:7]} : // S-Type
	  {{20{instruction[31]}}, instruction[31:20]} ; // I-Type
endmodule
