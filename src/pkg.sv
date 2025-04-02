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
    ALU_SLT = 3'b111 // Set if less than
  } alu_control_t;

endpackage
