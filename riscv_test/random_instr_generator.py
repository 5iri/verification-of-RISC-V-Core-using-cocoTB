import random
import cocotb
from cocotb.triggers import RisingEdge, Timer

# Define the instruction set with expected results
INSTRUCTION_SET = [
    (0x00100093, 1),  # ADDI x1, x0, 1 ----> output = 1
    (0x00008133, 1),  # ADD x2, x1, x0 ----> output = 1
    (0x001101b3, 2),  # ADD x3, x1, x1 ----> output = 2
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

    # Wait for some cycles to process the instructions
    await Timer(10, units="ns")
    assert dut.rvsingle.registerfile_0.register_file[1].value.integer == 1

    await Timer(10, units="ns")
    assert (dut.rvsingle.registerfile_0.register_file[2].value.integer) == 1

    await Timer(10, units="ns")
    assert (dut.rvsingle.registerfile_0.register_file[3].value.integer) == 2
    
