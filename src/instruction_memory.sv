`default_nettype none
module instruction_memory #(
    parameter WORDS = 64,
    parameter MEM_INIT_FILENAME = ""
) (
    input logic [31:0] read_address,
    input logic reset_n,
    input logic clk,
    output logic [31:0] instruction
);


  logic [31:0] memory[WORDS-1];  // Memory containing WORDS elements of 32-bit

  initial begin
    if (MEM_INIT_FILENAME != "") begin
      $readmemh(MEM_INIT_FILENAME, memory);
    end
  end

  always_comb begin
    instruction = memory[read_address[31:2]];  // use word index
  end

  always_ff @(posedge clk) begin
    if (reset_n == 0) begin
      for (int i = 0; i < WORDS; i++) begin
        memory[i] <= 32'b0;
      end
    end
  end

endmodule
