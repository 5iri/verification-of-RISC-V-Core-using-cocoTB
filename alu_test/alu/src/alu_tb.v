`timescale 1ns / 1ps

module alu_tb;
    reg [31:0] rs1;
    reg [31:0] rs2;
    reg [15:0] instructions;
    wire [63:0] ALUoutput;

    // Instantiate the ALU
    alu ALU1(.in1(rs1), .in2(rs2), .instructions(instructions), .ALUoutput(ALUoutput));

    initial begin
        // Initialize inputs
        rs1 = ~32'd5 + 1; // rs1 = -5 (in 2's complement)
        rs2 = 32'd4;
        instructions = 16'd0;

        // Test different operations
        #50 instructions = 16'd1;   // add
        if (ALUoutput == rs1 + rs2) $display("ADD: PASS | Expected: %h, Got: %h", rs1 + rs2, ALUoutput);
        else $display("ADD: FAIL | Expected: %h, Got: %h", rs1 + rs2, ALUoutput);

        #50 instructions = 16'd2;   // sub
        if (ALUoutput == rs1 - rs2) $display("SUB: PASS | Expected: %h, Got: %h", rs1 - rs2, ALUoutput);
        else $display("SUB: FAIL | Expected: %h, Got: %h", rs1 - rs2, ALUoutput);

        #50 instructions = 16'd4;   // xor
        if (ALUoutput == (rs1 ^ rs2)) $display("XOR: PASS | Expected: %h, Got: %h", rs1 ^ rs2, ALUoutput);
        else $display("XOR: FAIL | Expected: %h, Got: %h", rs1 ^ rs2, ALUoutput);

        #50 instructions = 16'd8;   // or
        if (ALUoutput == (rs1 | rs2)) $display("OR: PASS | Expected: %h, Got: %h", rs1 | rs2, ALUoutput);
        else $display("OR: FAIL | Expected: %h, Got: %h", rs1 | rs2, ALUoutput);

        #50 instructions = 16'd16;  // and
        if (ALUoutput == (rs1 & rs2)) $display("AND: PASS | Expected: %h, Got: %h", rs1 & rs2, ALUoutput);
        else $display("AND: FAIL | Expected: %h, Got: %h", rs1 & rs2, ALUoutput);

        #50 instructions = 16'd32;  // sll
        if (ALUoutput == (rs1 << rs2)) $display("SLL: PASS | Expected: %h, Got: %h", rs1 << rs2, ALUoutput);
        else $display("SLL: FAIL | Expected: %h, Got: %h", rs1 << rs2, ALUoutput);

        #50 instructions = 16'd64;  // srl
        if (ALUoutput == (rs1 >> rs2)) $display("SRL: PASS | Expected: %h, Got: %h", rs1 >> rs2, ALUoutput);
        else $display("SRL: FAIL | Expected: %h, Got: %h", rs1 >> rs2, ALUoutput);

        #50 instructions = 16'd128; // sra
        if (ALUoutput == (rs1 >>> rs2)) $display("SRA: PASS | Expected: %h, Got: %h", rs1 >>> rs2, ALUoutput);
        else $display("SRA: FAIL | Expected: %h, Got: %h", rs1 >>> rs2, ALUoutput);

        #50 instructions = 16'd256; // slt (signed)
        if (ALUoutput == ($signed(rs1) < $signed(rs2))) $display("SLT: PASS | Expected: %h, Got: %h", ($signed(rs1) < $signed(rs2)), ALUoutput);
        else $display("SLT: FAIL | Expected: %h, Got: %h", ($signed(rs1) < $signed(rs2)), ALUoutput);

        #50 instructions = 16'd512; // sltu (unsigned)
        if (ALUoutput == (rs1 < rs2)) $display("SLTU: PASS | Expected: %h, Got: %h", (rs1 < rs2), ALUoutput);
        else $display("SLTU: FAIL | Expected: %h, Got: %h", (rs1 < rs2), ALUoutput);

        #50 instructions = 16'd1024;// mul
        if (ALUoutput == (rs1 * rs2)) $display("MUL: PASS | Expected: %h, Got: %h", rs1 * rs2, ALUoutput);
        else $display("MUL: FAIL | Expected: %h, Got: %h", rs1 * rs2, ALUoutput); $finish;

        #50 instructions = 16'd2048;// div
        if (rs2 == 0) $display("DIV: SKIPPED (Division by zero)");
        else if (ALUoutput == ($signed(rs1) / $signed(rs2))) $display("DIV: PASS | Expected: %h, Got: %h", $signed(rs1) / $signed(rs2), ALUoutput);
        else $display("DIV: FAIL | Expected: %h, Got: %h", $signed(rs1) / $signed(rs2), ALUoutput); $finish;

        #50 instructions = 16'd4096;// rem
        if (rs2 == 0) $display("REM: SKIPPED (Division by zero)");
        else if (ALUoutput == ($signed(rs1) % $signed(rs2))) $display("REM: PASS | Expected: %h, Got: %h", $signed(rs1) % $signed(rs2), ALUoutput);
        else $display("REM: FAIL | Expected: %h, Got: %h", $signed(rs1) % $signed(rs2), ALUoutput); $finish;

        // Test signed comparison edge cases
        #50 rs1 = -5; rs2 = 3; instructions = 16'd256; // slt test
        if (ALUoutput == ($signed(rs1) < $signed(rs2))) $display("SLT (Edge Case): PASS | Expected: %h, Got: %h", ($signed(rs1) < $signed(rs2)), ALUoutput);
        else $display("SLT (Edge Case): FAIL | Expected: %h, Got: %h", ($signed(rs1) < $signed(rs2)), ALUoutput); $finish;

        #50 rs1 = -5; rs2 = 3; instructions = 16'd512; // sltu test
        if (ALUoutput == (rs1 < rs2)) $display("SLTU (Edge Case): PASS | Expected: %h, Got: %h", (rs1 < rs2), ALUoutput);
        else $display("SLTU (Edge Case): FAIL | Expected: %h, Got: %h", (rs1 < rs2), ALUoutput); $finish;

        // Test division by zero (should handle properly in ALU)
        #50 rs1 = 10; rs2 = 0; instructions = 16'd2048; // div by zero
        if (rs2 == 0) $display("DIV (Division by Zero): SKIPPED");
        else if (ALUoutput == ($signed(rs1) / $signed(rs2))) $display("DIV (Division by Zero): PASS | Expected: %h, Got: %h", $signed(rs1) / $signed(rs2), ALUoutput);
        else $display("DIV (Division by Zero): FAIL | Expected: %h, Got: %h", $signed(rs1) / $signed(rs2), ALUoutput); $finish;

        #50 rs1 = 10; rs2 = 0; instructions = 16'd4096; // rem by zero
        if (rs2 == 0) $display("REM (Division by Zero): SKIPPED");
        else if (ALUoutput == ($signed(rs1) % $signed(rs2))) $display("REM (Division by Zero): PASS | Expected: %h, Got: %h", $signed(rs1) % $signed(rs2), ALUoutput);
        else $display("REM (Division by Zero): FAIL | Expected: %h, Got: %h", $signed(rs1) % $signed(rs2), ALUoutput); $finish;

    end
endmodule