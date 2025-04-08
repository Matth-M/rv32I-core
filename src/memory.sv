`default_nettype none
module memory #(
    parameter integer WORDS = 64,
    parameter MEM_INIT_FILENAME = ""
) (
    input logic [31:0] address,
    input logic [31:0] write_data,
    input logic reset_n,
    input logic clk,
    input logic write_enable,
    output logic [31:0] data
);


  initial begin
    if (MEM_INIT_FILENAME != "") begin
      $readmemh(MEM_INIT_FILENAME, memory);
    end
  end

  logic [31:0] memory[WORDS-1];  // Memory containing WORDS elements of 32-bit

  always_comb begin
    data = memory[address[31:2]];  // use word index
  end

  always_ff @(posedge clk) begin
    if (reset_n == 0) begin
      for (int i = 0; i < WORDS; i++) begin
        memory[i] <= 32'b0;
      end
      // Address should be words boundaries aligned, meaning address
      // should be a multiple of 4 (4 bytes in a 32-bit word)
    end else if (write_enable == 1 && address[1:0] == 2'b00) begin
      memory[address[31:2]] <= write_data;  // use word index
    end
  end

endmodule
