/**
 * @file riscv_cpu.v
 * 
 * This module implements the bare cpu modules, and interconnects various signals
 * of modules.
 * 
 * @input clk         Inputs clock signal.
 * @input reset       Inputs reset signal.
 * @input Instr       Inputs Instruction from instruction memory.
 * @input ReadData    Input Data read from memory.
 *
 * @return PC         Output program counter value.
 * @return MemWrite   Output memory write enable signal.
 * @return Mem_WrAddr Output memory write enable address.
 * @return Mem_WrData Output data to be written to memory.
*/


module riscv_cpu (
  input clk, reset,
    output [31:0] PC,
    input  [31:0] Instr,
    output MemWrite,
    output [31:0] Mem_WrAddr, Mem_WrData,
    input  [31:0] ReadData
);
wire Jump_sign;
wire [31:0] Jump_ADDR;
wire [31:0] IMM_ADDR;
wire [12:0] alu_instruction;
wire [31:0] ProgramCounter;
wire [31:0] source_val1;
wire [31:0] source_val2;
wire [63:0] ALUoutput;
wire [6:0] opcode;
wire [44:0] out_signal;
wire rs1_valid;
wire rs2_valid;
wire registerfile_write;
wire [31:0] destination_register;
wire [31:0] final_output;
wire [4:0] rs1;
wire [4:0] rs2;
wire [31:0] input_val1;
wire [31:0] input_val2;
assign PC = ProgramCounter;
PC b2v_inst(
    .clk(clk),
    .reset(reset),
    .j_signal(Jump_sign),
    .jump(Jump_ADDR),
    .out_sign(ProgramCounter));
alu b2v_inst1(
    .instructions(alu_instruction),
    .in1(input_val1),
    .in2(input_val2),
    .ALUoutput(ALUoutput));
control_unit b2v_inst2(
    .clk(clk),
    .rst(reset),
    .ALUoutput(ALUoutput),
    .imm(IMM_ADDR),
    .mem_read(ReadData),
    .opcode(opcode),
    .out_signal(out_signal),
    .pc_input(ProgramCounter),
    .rs1_input(source_val1),
    .rs2_input(source_val2),
    .j_signal(Jump_sign),
    .wr_en_rf(registerfile_write),
    .wr_en(MemWrite),
    .addr(Mem_WrAddr),
    .final_output(final_output),
    .instructions(alu_instruction),
    .v1(input_val1),
    .v2(input_val2),
    .jump(Jump_ADDR),
    .mem_write(Mem_WrData));
decoder b2v_inst3(
    .instr(Instr),
    .rs1_valid(rs1_valid),
    .rs2_valid(rs2_valid),
    .imm(IMM_ADDR),
    .opcode(opcode),
    .out_signal(out_signal),
    .rd(destination_register[4:0]),
    .rs1(rs1),
    .rs2(rs2));
registerfile registerfile_0(
    .clk(clk),
    .rs1_valid(rs1_valid),
    .rs2_valid(rs2_valid),
    .wr_en(registerfile_write),
    .rd(destination_register),
    .rd_value(final_output),
    .rs1(rs1),
    .rs2(rs2),
    .rs1_value(source_val1),
    .rs2_value(source_val2));
endmodule
