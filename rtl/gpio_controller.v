module gpio_4pins (
    input wire clk,
    input wire reset,
    input wire [1:0] IOAdr,         // 2-bit address to select one of the 4 GPIO pins
    input wire WriteIO,
    input wire [3:0] IOWrite,       // Data to write to GPIO pins
    inout wire [3:0] gpio_pins      // 4 bi-directional GPIO pins
);
    reg [3:0] gpio_data;            // Holds the output state of GPIO pins

    // Tri-state buffers for each GPIO pin
    assign gpio_pins[0] = gpio_data[0];
    assign gpio_pins[1] = gpio_data[1];
    assign gpio_pins[2] = gpio_data[2];
    assign gpio_pins[3] = gpio_data[3]; 

    // Write logic
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            gpio_data <= 4'b0;
        end else if (WriteIO) begin
            case (IOAdr)
                2'd0: gpio_data[0] <= IOWrite[0];
                2'd1: gpio_data[1] <= IOWrite[1];
                2'd2: gpio_data[2] <= IOWrite[2];
                2'd3: gpio_data[3] <= IOWrite[3];
                default: ; // Do nothing
            endcase
        end
    end
endmodule


module gpio_28pins (
    input wire clk,
    input wire reset,
    input wire [4:0] IOAdr,          // 5-bit address to select one of 28 GPIO pins
    input wire WriteIO,             // Write enable signal
    input wire [31:0] IOWrite,      // Data to write to GPIO pins
    inout wire [27:0] gpio_pins     // 28 bi-directional GPIO pins
);
    // Internal wires to connect the submodules
    wire [3:0] gpio_pins_group[6:0];

    // Instances of gpio_4pins
    gpio_4pins group0 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd0)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[0])
    );

    gpio_4pins group1 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd1)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[1])
    );

    gpio_4pins group2 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd2)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[2])
    );

    gpio_4pins group3 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd3)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[3])
    );

    gpio_4pins group4 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd4)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[4])
    );

    gpio_4pins group5 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd5)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[5])
    );

    gpio_4pins group6 (
        .clk(clk),
        .reset(reset),
        .IOAdr(IOAdr[1:0]),
        .WriteIO(WriteIO && (IOAdr[4:2] == 3'd6)),
        .IOWrite(IOWrite[3:0]),
        .gpio_pins(gpio_pins_group[6])
    );

    // Combine the outputs of the submodules into one 28-pin bus
    assign gpio_pins[3:0]    = gpio_pins_group[0];
    assign gpio_pins[7:4]    = gpio_pins_group[1];
    assign gpio_pins[11:8]   = gpio_pins_group[2];
    assign gpio_pins[15:12]  = gpio_pins_group[3];
    assign gpio_pins[19:16]  = gpio_pins_group[4];
    assign gpio_pins[23:20]  = gpio_pins_group[5];
    assign gpio_pins[27:24]  = gpio_pins_group[6];

endmodule
