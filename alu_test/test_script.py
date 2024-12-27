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
    for i in range(100000):
        in1 = random.randint(0, 2147483647)  # Random 31-bit signed integer
        in2 = random.randint(0, in1)
        instructions = random.randint(0, 4095)

        # Apply inputs
        dut.in1.value = in1
        dut.in2.value = in2
        dut.instructions.value = instructions

        # Allow some time for propagation
        await Timer(1, units="ns")

        # Compute expected result
        if instructions == ADD_INSTR:
            expected_result = in1 + in2
        elif instructions == SUB_INSTR:
            expected_result = in1 - in2
        elif instructions == AND_INSTR:
            expected_result = in1 & in2
        elif instructions == OR_INSTR:
            expected_result = in1 | in2
        elif instructions == XOR_INSTR:
            expected_result = in1 ^ in2
        elif instructions == SLL_INSTR:
            expected_result = in1 << (in2 & 0x1F)  # Mask to 5 bits
        elif instructions == SRL_INSTR:
            expected_result = in1 >> (in2 & 0x1F)  # Logical right shift
        elif instructions == SRA_INSTR:
            expected_result = in1 >> (in2 & 0x1F) if in1 >= 0 else (~((~in1) >> (in2 & 0x1F)))
        elif instructions == SLT_INSTR:
            expected_result = int(in1 < in2)
        elif instructions == SLTU_INSTR:
            expected_result = int((in1 & 0xFFFFFFFF) < (in2 & 0xFFFFFFFF))
        elif instructions == MUL_INSTR:
            expected_result = (in1 * in2) & 0xFFFFFFFF  # Lower 32 bits only
        elif instructions == DIV_INSTR:
            expected_result = in1 // in2 if in2 != 0 else 0  # Handle division by zero
        elif instructions == REM_INSTR:
            expected_result = in1 % in2 if in2 != 0 else 0  # Handle division by zero
        else:
            expected_result = 0

        # Fetch the signed integer from the ALUoutput
        actual_result = dut.ALUoutput.value.signed_integer

        # For MUL_INSTR, compare only the lower 32 bits
        if instructions == MUL_INSTR:
            assert (actual_result & 0xFFFFFFFF) == expected_result, (
                f"Test failed for instruction {instructions} (MUL): "
                f"in1={in1}, in2={in2}, expected (lower 32 bits)={expected_result}, "
                f"got={actual_result & 0xFFFFFFFF}"
            )
        else:
            # For all other instructions, compare the full result
            assert actual_result == expected_result, (
                f"Test failed for instruction {instructions}: "
                f"in1={in1}, in2={in2}, expected={expected_result}, got={actual_result}"
            )
    print("All ALU tests passed successfully!")
