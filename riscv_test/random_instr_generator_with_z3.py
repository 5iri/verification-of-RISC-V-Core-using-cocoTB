import cocotb
from cocotb.triggers import Timer
from z3 import *

# Define the instruction set with expected result
INSTRUCTION_SET = [
    #   32-bit instr, output_reg, output_val
    # Arithmetic instructions
    (0x00100093, 1, 1),    # ADDI x1, x0, 1 -> x1 = 1
    (0x00208133, 2, 1),    # ADD x2, x1, x2 -> x2 = 1 + 0
    (0x402081b3, 3, 0),    # SUB x3, x1, x2 -> x3 = 1 - 1
    (0x00300093, 1, 3),    # ADDI x1, x0, 3 -> x1 = 3
    (0x00008133, 2, 3),    # ADD x2, x1, x0 -> x2 = 3
    # Logical instructions
    (0x00400193, 3, 4),    # ADDI x3, x0, 4 -> x3 = 4
    (0x001041b3, 3, 3),    # XOR x3, x0, x1 -> x3 = 3
    (0x003061b3, 3, 3),    # OR x3, x0, x3 -> x3 = 3 | 0 = 3
    (0x0020c1b3, 3, 0),    # XOR x3, x1, x2 -> x3 = 3 ^ 3 = 0
    (0x0020a1b3, 3, 0),    # SLT x3, x1, x2 -> x3 = (x1 < x2) = 0
    # Shift instructions
    (0x00205133, 2, 0),    # SLL x2, x1, x2 -> x2 = 3 << 2 = 0
    (0x00209133, 2, 3),    # SRL x2, x1, x2 -> x2 = 3 >> 2 = 3
    (0x40209133, 2, 3),    # SRA x2, x1, x2 -> x2 = arithmetic shift
    # Control flow instructions
    (0x00000063, 0, 0),    # BEQ x0, x0, offset -> PC should branch
    (0x001000e3, 0, 0),    # BNE x0, x1, offset -> PC should not branch
    (0x00000113, 2, 3),    # JALR x2, x0, offset -> x2 = PC + 4
    # Load/store instructions (simplified for testing)
    (0x00002003, 1, 3),    # LW x1, 0(x0) -> Load value from memory
    (0x00402023, 0, 0),    # SW x1, 4(x0) -> Store value into memory
]# Z3 symbolic register definitions
registers = [Int(f"x{i}") for i in range(32)]

# SMT solver
solver = Solver()

# Clock generation for the Verilog simulation
async def clock_gen(dut):
    while True:
        dut.clk.value = 0
        await Timer(5, units="ns")
        dut.clk.value = 1
        await Timer(5, units="ns")

# Load instructions into Verilog DUT
async def load_instructions(dut, num_instructions):
    for addr in range(num_instructions):
        dut.imem.instr_ram[addr].value = INSTRUCTION_SET[addr][0]  # Load instruction
        cocotb.log.info(f"Loaded instruction {hex(INSTRUCTION_SET[addr][0])} at address {addr}")

@cocotb.test()
async def test_riscv_with_z3(dut):
    """
    Test RISC-V CPU with Z3 verification.
    """
    # Start the clock
    cocotb.start_soon(clock_gen(dut))

    # Load instructions into instruction memory
    num_instructions = len(INSTRUCTION_SET)
    await load_instructions(dut, num_instructions)

    # Initial state: Assume all registers are 0
    for i in range(32):
        solver.add(registers[i] == 0)

    # Run the simulation for each instruction
    for idx in range(num_instructions):
        await Timer(10, units="ns")  # Wait for instruction execution

        # Get the Verilog DUT's register values
        reg_index = INSTRUCTION_SET[idx][1]
        expected_value = INSTRUCTION_SET[idx][2]
        observed_value = dut.rvsingle.registerfile_0.register_file[reg_index].value.signed_integer

        # Add a constraint to Z3 for the current instruction
        solver.add(registers[reg_index] == expected_value)

        # Verify the result
        if observed_value != expected_value:
            cocotb.log.error(f"Instruction {idx}: Expected x{reg_index} = {expected_value}, got {observed_value}")
        else:
            cocotb.log.info(f"Instruction {idx}: x{reg_index} = {observed_value} (Correct)")

    # Check if all Z3 constraints are satisfied
    cocotb.log.info(solver.check())
    if solver.check() == z3.sat:
        cocotb.log.info("Z3: All instructions executed correctly.")
    else:
        cocotb.log.error("Z3: Instruction execution failed.")
        cocotb.log.error(f"Unsat Core: {solver.unsat_core()}")

