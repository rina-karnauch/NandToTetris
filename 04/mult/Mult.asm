// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// counter setting to RAM[0]
@R0
D=M
@counter
M=D

// setting the value to add 
@R1
D=M
@value
M=D

// mul setting
@R2
M=0
@mul
M=0

(LOOP)
    @counter // we set the counter inside D and we make it smaller each time- looping
    D=M
    @END
    D;JLE // if we reached smaller than 0 than we stop. 
    // ^ we run while counter > 0

    @value
    D=M
    // ^ the value we are adding counter times.

    @mul
    M=D+M
    D=M
    @R2
    M=D
    // ^ the adding process

    @counter
    M=M-1
    D=M
    // ^ making the loop smaller

    @LOOP
    D;JGT

(END)

