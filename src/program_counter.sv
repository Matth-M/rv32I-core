`default_nettype none
module program_counter (
	input logic [31:0] pc_next,
	input logic clk,
	input logic reset_n,
	output logic [31:0] pc
);

  always_ff @(posedge clk) begin
	  if (reset_n == 0) begin
		  pc <= 32'b0;
	  end else begin
		  pc <= pc_next;
	  end
  end

endmodule
