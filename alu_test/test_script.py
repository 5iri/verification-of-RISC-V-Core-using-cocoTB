import random
import cocotb
from cocotb.triggers import Timer

# Define ALU operation opcodes for easier readability
ADD_INSTR = 1
SUB_INSTR = 2
AND_INSTR = 16
OR_INSTR = 8
XOR_INSTR = 4
SLL_INSTR = 32
SRL_INSTR = 64
SRA_INSTR = 128
SLT_INSTR = 256
SLTU_INSTR = 512
MUL_INSTR = 1024
DIV_INSTR = 2048
REM_INSTR = 4096

@cocotb.test()
async def alu_full_operations(dut):
    """Testing all ALU operations defined in RV32IM"""

    # Initialize inputs
    dut.in1.value = 0
    dut.in2.value = 0
    dut.instructions.value = 0

    # Test random cases
    for i in range(10000):
        in1 = random.randint(0, 2_147_483_647)  # Random 32-bit signed integer
        in2 = random.randint(0, 2_147_483_647)
        if in1 > in2:
            instruction = random.choice([
                ADD_INSTR, SUB_INSTR, AND_INSTR, OR_INSTR, XOR_INSTR,
                SLL_INSTR, SRL_INSTR, SRA_INSTR, SLT_INSTR, SLTU_INSTR,
                MUL_INSTR, DIV_INSTR, REM_INSTR
            ])
        else:
            instruction = random.choice([
                ADD_INSTR, AND_INSTR, OR_INSTR, XOR_INSTR,
                SLL_INSTR, SRL_INSTR, SRA_INSTR, SLT_INSTR, SLTU_INSTR,
                MUL_INSTR, DIV_INSTR, REM_INSTR
            ])


        # Apply inputs
        dut.in1.value = in1
        dut.in2.value = in2
        dut.instructions.value = instruction

        # Allow some time for propagation
        await Timer(1, units="ns")

        # Compute expected result
        if instruction == ADD_INSTR:
            expected_result = in1 + in2
        elif instruction == SUB_INSTR:
            expected_result = in1 - in2
        elif instruction == AND_INSTR:
            expected_result = in1 & in2
        elif instruction == OR_INSTR:
            expected_result = in1 | in2
        elif instruction == XOR_INSTR:
            expected_result = in1 ^ in2
        elif instruction == SLL_INSTR:
            expected_result = in1 << (in2 & 0x1F)  # Mask to 5 bits
        elif instruction == SRL_INSTR:
            expected_result = in1 >> (in2 & 0x1F)  # Logical right shift
        elif instruction == SRA_INSTR:
            expected_result = in1 >> (in2 & 0x1F) if in1 >= 0 else (~((~in1) >> (in2 & 0x1F)))
        elif instruction == SLT_INSTR:
            expected_result = int(in1 < in2)
        elif instruction == SLTU_INSTR:
            expected_result = int((in1 & 0xFFFFFFFF) < (in2 & 0xFFFFFFFF))
        elif instruction == MUL_INSTR:
            expected_result = in1 * in2
        elif instruction == DIV_INSTR:
            expected_result = in1 // in2 if in2 != 0 else 0  # Handle division by zero
        elif instruction == REM_INSTR:
            expected_result = in1 % in2 if in2 != 0 else 0  # Handle division by zero
        else:
            expected_result = 0

        # Validate output
        assert dut.ALUoutput.value == expected_result, \
            f"Test failed for instruction {instruction}: in1={in1}, in2={in2}, expected={expected_result}, got={int(dut.ALUoutput.value)}"

    print("All ALU tests passed successfully!")
