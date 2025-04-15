`default_nettype none
import pkg::*;
module control (
    input logic [6:0] opcode,
    input logic [2:0] funct3,
    input logic [6:0] funct7,
    input logic alu_zero,
    output logic reg_write_enable,
    output logic data_mem_write_enable,
    output logic alu_src,
    output logic result_src,
    output logic branch,
    output logic [1:0] imm_src,
    output logic [3:0] alu_control
);

  // Tells the alu decoder which instruction to indicate
  logic [1:0] alu_op;

  // Main decoder
  always_comb begin
    reg_write_enable = 0;
    imm_src = 2'b00;
    alu_src = 0;
    data_mem_write_enable = 0;
    result_src = 0;
    branch = 0;
    alu_op = 2'b00;
    case (opcode)
      OPCODE_I_TYPE_LOAD: begin
        reg_write_enable = 1;
        imm_src = 2'b00;
        alu_src = 1;
        data_mem_write_enable = 0;
        result_src = 1;
        branch = 0;
        alu_op = ALU_OP_LOAD_STORE;
      end
      OPCODE_S_TYPE: begin
        reg_write_enable = 0;
        imm_src = IMM_SRC_S_TYPE;
        alu_src = 1;
        data_mem_write_enable = 1;
        branch = 0;
        alu_op = ALU_OP_LOAD_STORE;
      end
      OPCODE_I_TYPE_ALU: begin
        reg_write_enable = 1;
        imm_src = IMM_SRC_I_TYPE;
        alu_src = 1;
        data_mem_write_enable = 0;
        result_src = 0;
        branch = 0;
        alu_op = ALU_OP_MATH;
      end
      OPCODE_R_TYPE: begin
        reg_write_enable = 1;
        alu_src = 0;
        data_mem_write_enable = 0;
        result_src = 0;
        branch = 0;
        alu_op = ALU_OP_MATH;
      end
      default: begin
        reg_write_enable = 0;
        imm_src = 2'b00;
        alu_src = 0;
        data_mem_write_enable = 0;
        result_src = 0;
        branch = 0;
        alu_op = 2'b00;
      end
    endcase
  end

  // ALU decoder
  always_comb begin
    case (alu_op)
      ALU_OP_LOAD_STORE: alu_control = ALU_ADD;
      ALU_OP_BRANCH: alu_control = ALU_SUB;
      ALU_OP_MATH: begin
        if (funct3 == FUN3_ADD_SUB) begin
          if ({opcode[5], funct7[5]} == 2'b11) begin
            alu_control = ALU_SUB;
          end else begin
            alu_control = ALU_ADD;
          end
        end else if (funct3 == FUN3_XOR) begin
          alu_control = ALU_XOR;
        end else if (funct3 == FUN3_OR) begin
          alu_control = ALU_OR;
        end else if (funct3 == FUN3_AND) begin
          alu_control = ALU_AND;
        end else if (funct3 == FUN3_SLL) begin
          alu_control = ALU_SLL;
        end else if (funct3 == FUN3_SRL_SRA) begin
          if (funct7 == 7'h20) begin
            alu_control = ALU_SRA;
          end else if (funct7 == 7'b0) begin
            alu_control = ALU_SRL;
          end else begin
            alu_control = 4'b0000;
          end
        end else if (funct3 == FUN3_SLT) begin
          alu_control = ALU_SLT;
        end else if (funct3 == FUN3_SLTU) begin
          alu_control = ALU_SLTU;
        end else begin
          alu_control = 4'b0000;
        end
      end
      default: alu_control = 4'b0000;
    endcase
  end


endmodule
