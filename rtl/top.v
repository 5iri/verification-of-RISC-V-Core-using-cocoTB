module top (
    input clk_in, reset,
    output led1, led2, led3, led4, led5, led6, led7, led8
);
    // Clock signal for the system
    wire clk;
    clock_divider_100M_to_1Hz slow_clock_gen (.clk_in(clk_in), .reset(reset), .clk(clk));

    // Processor and memory signals
    wire [31:0] PC;
    wire [31:0] Instr;
    wire MemWrite_rv32;
    wire [31:0] DataAdr_rv32, WriteData_rv32;
    reg [31:0] ReadData;
    // GPIO interface signals
    wire [4:0] IOAdr;
    wire [31:0] WriteIO;
    wire [31:0] ReadIO;
    wire IOWrite;
    wire [27:0] gpio_pins;

    // Instantiate processor and memories
    riscv_cpu rvsingle (
        .clk(clk),
        .reset(reset),
        .PC(PC),
        .Instr(Instr),
        .MemWrite(MemWrite_rv32),
        .Mem_WrAddr(DataAdr_rv32),
        .Mem_WrData(WriteData_rv32),
        .ReadData(ReadData)
    );

    instr_mem imem (
        .instr_addr(PC),
        .instr(Instr)
    );

    data_mem dmem (
        .clk(clk),
        .wr_en(MemWrite),
        .wr_addr(DataAdr),
        .wr_data(WriteData),
        .rd_data_mem(ReadData_mem)
    );

    // Instantiate GPIO module
    gpio_28pins io (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr),
        .WriteIO(WriteIO),
        .IOWrite(IOWrite),
        .gpio_pins(gpio_pins)
    );

    // Address and data multiplexing
    always @* begin
        if (DataAdr_rv32 >= 32'h03000000) begin
            ReadData = ReadIO; // Read from GPIO
        end else begin
            ReadData = ReadData; // Read from data memory
        end
    end

    // Control signals for memory and GPIO
    assign MemWrite = (DataAdr_rv32 < 32'h03000000) ? MemWrite_rv32 : 0;
    assign WriteData = (DataAdr_rv32 < 32'h03000000) ? WriteData_rv32 : 0;
    assign DataAdr = (DataAdr_rv32 < 32'h03000000) ? DataAdr_rv32 : 0;

    assign IOWrite = (DataAdr_rv32 >= 32'h03000000) ? MemWrite_rv32 : 0;
    assign IOAdr = (DataAdr_rv32 >= 32'h03000000) ? DataAdr_rv32[4:0] : 0;
    assign WriteIO = (DataAdr_rv32 >= 32'h03000000) ? WriteData_rv32 : 0;

    // Map GPIO pins to LED outputs
    assign {led8, led7, led6, led5, led4, led3, led2, led1} = gpio_pins[7:0];

endmodule

// Clock Divider Module
module clock_divider_100M_to_1Hz (
    input wire clk_in,   // 100 MHz input clock
    input wire reset,    // Reset signal
    output reg clk       // 1 Hz output clock
);

    // Define the counter limit for 100MHz to 1Hz conversion
    localparam COUNTER_LIMIT = 50_000_000; // 100 MHz / 2 for a full cycle

    reg [25:0] counter; // 26-bit counter (log2(50M) = ~26)

    always @(posedge clk_in or posedge reset) begin
        if (reset) begin
            counter <= 0;
            clk <= 0;
        end else begin
            if (counter == COUNTER_LIMIT - 1) begin
                counter <= 0;
                clk <= ~clk; // Toggle the output clock
            end else begin
                counter <= counter + 1;
            end
        end
    end

endmodule
