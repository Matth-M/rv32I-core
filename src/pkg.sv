package pkg;
  // ALU control arithmetic
  typedef enum logic [2:0] {
    ALU_AND = 3'b000,
    ALU_OR = 3'b001,
    ALU_ADD = 3'b010,
    // ALU_XX   = 3'b011, // unused
    ALU_ANDNB = 3'b100,  // A & ~B
    ALU_ORNB = 3'b101,  // A | ~B
    ALU_SUB = 3'b110,
    ALU_SLT = 3'b111  // Set if less than
  } alu_control_t;

  typedef enum logic [1:0] {
    ALU_OP_LOAD_STORE = 2'b00,
    ALU_OP_BRANCH     = 2'b01,
    ALU_OP_MATH       = 2'b10
  } alu_op_t;

  typedef enum logic [2:0] {
    FUN3_ADD_SUB = 3'b000,
    FUN3_SLT = 3'b010,
    FUN3_OR = 3'b110,
    FUN3_AND = 3'b111
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
