import random
import cocotb
from cocotb.triggers import RisingEdge, Timer

# Define the instruction set
INSTRUCTION_SET = [
    0x00100093,  # ADDI x1, x0, 1 ----> output = 1
    0x00008133,  # ADD x2, x1, x0 ----> output = 1
    0x00108133,  # ADD x2, x1, x1 ----> output = 2
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
async def load_random_instructions(dut, num_instructions):
    '''
    Loading the random instructions into the DUT's instruction memory
    '''
    for addr in range(num_instructions):
        random_instr = random.choice(INSTRUCTION_SET)
        dut.imem.instr.value = random_instr  # Write instruction to instruction memory
        cocotb.log.info(f"Loaded instruction {hex(random_instr)} at address {addr}")

@cocotb.test()
async def test_random_instructions(dut):
    '''
    Testing the random instructions execution on the synapse32 CPU
    '''
    # Start the clock
    cocotb.start_soon(clock_gen(dut))

    # Frequency check variables
    time_first_edge = None
    time_second_edge = None

    # Wait for the first rising edge
    await RisingEdge(dut.clk)
    time_first_edge = cocotb.utils.get_sim_time(units="ns")

    # Wait for the second rising edge
    await RisingEdge(dut.clk)
    time_second_edge = cocotb.utils.get_sim_time(units="ns")

    # Calculate the clock period
    clock_period = time_second_edge - time_first_edge
    clock_frequency = 1e9 / clock_period  # Convert period (ns) to frequency (Hz)

    # Log the clock frequency
    cocotb.log.info(f"Measured Clock Period: {clock_period} ns")
    cocotb.log.info(f"Measured Clock Frequency: {clock_frequency} Hz")

    # Assert the clock frequency is close to 100 MHz
    assert abs(clock_frequency - 100e6) < 1e3, "Clock frequency is not 100 MHz!"

    # Load instructions into instruction memory
    num_instructions = 3  # Number of instructions to load
    await load_random_instructions(dut, num_instructions)

    # Wait for some cycles to ensure the DUT processes the instructions
    await Timer(100, units="ns")

    cocotb.log.info("Instruction memory testing completed. Ready to test the RISC-V CPU module.")



    #until now, tested only if the instruction has gone into imem and if the clk is working or nah



    
