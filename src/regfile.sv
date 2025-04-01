`default_nettype none
module regfile (
    input logic [4:0] read_address1,
    input logic [4:0] read_address2,
    input logic [4:0] write_address,
    input logic [31:0] write_data,
    input logic write_enable,
    input logic clk,
    input logic reset_n,
    output logic [31:0] read_data1,
    output logic [31:0] read_data2
);

  logic [31:0] registers[32];

  always_ff @(posedge clk) begin
    if (reset_n == 0) begin
      for (int i = 0; i < 32; i++) begin
        registers[i] <= 32'b0;
      end
    end
    if (write_enable && write_address != 0) begin
      registers[write_address] <= write_data;
    end
  end

  assign registers[0] = 32'b0;
  assign read_data1   = registers[read_address1];
  assign read_data2   = registers[read_address2];
endmodule
