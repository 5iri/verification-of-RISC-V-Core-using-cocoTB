import random
import cocotb
from cocotb.triggers import RisingEdge, Timer

# Define the instruction set with expected results
INSTRUCTION_SET = [

#   32-bit instr, output_reg, output_val
    # Arithmetic instructions
    (0x00100093, 1, 1),    # ADDI x1, x0, 1 -> x1 = 1
    (0x00208133, 2, 1),    # ADD x2, x1, x2 -> x2 = 1 + 0
    (0x402081b3, 3, 0),   # SUB x3, x1, x2 -> x3 = 1 - 1
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
    (0x40209133, 2, 3),   # SRA x2, x1, x2 -> x2 = arithmetic shift

    # Control flow instructions
    (0x00000063, 0, 0),    # BEQ x0, x0, offset -> PC should branch
    (0x001000e3, 0, 0),    # BNE x0, x1, offset -> PC should not branch
    (0x00000113, 2, 3),    # JALR x2, x0, offset -> x2 = PC + 4

    # Load/store instructions (simplified for testing)
    (0x00002003, 1, 3),  # LW x1, 0(x0) -> Load value from memory
    (0x00402023, 0, 0),    # SW x1, 4(x0) -> Store value into memory
]

# Clock generation for 100 MHz
async def clock_gen(dut):
    '''
    Generates a clock with a period of 10 ns (100 MHz)
    '''
    while True:
        dut.clk.value = 0
        await Timer(5, units="ns")
        dut.clk.value = 1
        await Timer(5, units="ns")

# Helper function to load random instructions into the DUT
async def load_instructions(dut, num_instructions):
    '''
    Loading the instructions into the DUT's instruction memory
    '''
    for addr in range(num_instructions):
        dut.imem.instr_ram[addr].value = INSTRUCTION_SET[addr][0]  # Write instruction to instruction memory
        cocotb.log.info(f"Loaded instruction {hex(INSTRUCTION_SET[addr][0])} at address {addr}")

@cocotb.test()
async def test_instruction_results(dut):
    '''
    Testing the results of executing instructions on the synapse32 CPU
    '''
    # Start the clock
    cocotb.start_soon(clock_gen(dut))

    # Load instructions into instruction memory
    num_instructions = len(INSTRUCTION_SET)

    await load_instructions(dut, num_instructions)

    for idx in range(num_instructions):
        await Timer(10, units="ns")
        assert (dut.rvsingle.registerfile_0.register_file[INSTRUCTION_SET[idx][1]].value.signed_integer == INSTRUCTION_SET[idx][2])
