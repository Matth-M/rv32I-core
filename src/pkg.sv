package pkg;
  // ALU control arithmetic
  typedef enum logic [3:0] {
    ALU_ADD  = 4'b0000,
    ALU_SUB  = 4'b0001,
    ALU_XOR  = 4'b0010,
    ALU_OR   = 4'b0011,
    ALU_AND  = 4'b0100,
    ALU_SLL  = 4'b0101,
    ALU_SRL  = 4'b0110,
    ALU_SRA  = 4'b0111,
    ALU_SLT  = 4'b1000,
    ALU_SLTU = 4'b1001
  } alu_control_t;

  typedef enum logic [1:0] {
    ALU_OP_LOAD_STORE = 2'b00,
    ALU_OP_BRANCH     = 2'b01,
    ALU_OP_MATH       = 2'b10
  } alu_op_t;

  typedef enum logic [2:0] {
    FUN3_ADD_SUB = 3'b000,
    FUN3_XOR = 3'b100,
    FUN3_OR = 3'b110,
    FUN3_AND = 3'b111,
    FUN3_SLL = 3'b001,
    FUN3_SRL_SRA = 3'b101,
    FUN3_SLT = 3'b010,
    FUN3_SLTU = 3'b011
  } func3_t;


  typedef enum logic [6:0] {
    OPCODE_I_TYPE_LOAD = 7'b0000011,
    OPCODE_I_TYPE_ALU = 7'b0010011,
    OPCODE_I_TYPE_JALR = 7'b1100111,
    OPCODE_R_TYPE = 7'b0110011,
    OPCODE_S_TYPE = 7'b0100011,
    OPCODE_B_TYPE = 7'b1100011,
    OPCODE_J_TYPE = 7'b1101111
  } opcode_t;

  typedef enum logic [1:0] {
    IMM_SRC_I_TYPE = 2'b00,
    IMM_SRC_S_TYPE = 2'b01
  } imm_src_t;



endpackage
