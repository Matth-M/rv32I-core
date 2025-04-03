import pkg::*;
module cpu (
    input logic clk,
    input logic reset_n
);

  wire alu_src;
  wire result_src;
  wire [31:0] pc_next;
  wire [31:0] pc;
  wire [31:0] instruction;
  wire [4:0] regfile_read_address1;
  wire [4:0] regfile_read_address2;
  wire [4:0] regfile_write_address;
  wire [31:0] regfile_write_data;
  wire [31:0] read_data_registers1;
  wire [31:0] read_data_registers2;
  wire [1:0] imm_src;
  wire [31:0] imm_ext;
  wire [31:0] alu_srcA;
  logic [31:0] alu_srcB;
  wire [31:0] alu_result;
  wire [31:0] data_memory_value;
  wire [31:0] data_memory_write_data;
  wire [2:0] alu_control;
  wire regfile_write_enable;
  wire data_mem_write_enable;
  wire alu_zero;
  wire branch;


  // CONTROL

  control control (
      .opcode(instruction[6:0]),
      .funct3(instruction[14:12]),
      .funct7(instruction[31:25]),
      .alu_zero(alu_zero),
      .reg_write_enable(regfile_write_enable),
      .data_mem_write_enable(data_mem_write_enable),
      .alu_src(alu_src),
      .result_src(result_src),
      .branch(branch),
      .imm_src(imm_src),
      .alu_control(alu_control)
  );

  // DATAPATH

  assign pc_next = pc + 4;
  program_counter pc_inst (
      .pc_next(pc_next),
      .clk(clk),
      .reset_n(reset_n),
      .pc(pc)
  );

  instruction_memory #(
      .MEM_INIT_FILENAME("./instruction_memory.hex")
  ) instr_mem (
      .clk(clk),
      .reset_n(reset_n),
      .read_address(pc),
      .instruction(instruction)
  );

  assign regfile_read_address1 = instruction[19:15];
  assign regfile_read_address2 = instruction[24:20];
  assign regfile_read_address2 = instruction[11:7];
  assign regfile_write_data = result_src ? data_memory_value : alu_result;
  regfile registers (
      .clk(clk),
      .reset_n(reset_n),
      .write_enable(regfile_write_enable),
      .read_address1(regfile_read_address1),
      .read_address2(regfile_read_address2),
      .write_address(regfile_write_address),
      .write_data(regfile_write_data),
      .read_data1(read_data_registers1),
      .read_data2(read_data_registers2)
  );

  sign_extender sign_extend (
      .imm_src(imm_src),
      .instruction(instruction),
      .imm_ext(imm_ext)
  );

  always_comb begin
    if (alu_src) begin
      alu_srcB = imm_ext;
    end else alu_srcB = read_data_registers2;
  end
  alu alu (
      .srcA(alu_srcA),
      .srcB(alu_srcB),
      .alu_control(alu_control),
      .result(alu_result),
      .zero(alu_zero)
  );

  assign data_memory_write_data = read_data_registers2;
  data_memory data_mem (
      .clk(clk),
      .reset_n(reset_n),
      .address(alu_result),
      .write_data(32'b0),
      .write_enable(data_mem_write_enable),
      .data(data_memory_value)
  );
endmodule
