// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(PROGRAM)
    @8193
    D=A
    @counter
    M=D

    @SCREEN
    D=A
    @scr
    M=D

    @KEYBOARD
    D=M
    @pressed
    M=D

    @FILLER
    D;JNE
    @EMPTY
    D;JEQ

(FILLER)
    @value
    M=-1
    @FILLSCREEN
    0;JMP

(EMPTY)
    @value
    M=0
    @FILLSCREEN
    0;JMP

(FILLSCREEN)
    @counter
    M=M-1
    D=M
    @PROGRAM
    D;JLE

    @counter
    D=M

    @value
    D=M

    @scr
    A=M
    M=D

    @scr
    M=M+1   
    A=A+1
    @FILLSCREEN
    0;JMP

(END)

    