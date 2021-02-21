// The program's inputs will be at R13,R14 while the result R13/R14 should be stored at R15. Don't change the input registers.
// The remainder should be discarded: 3 divided by 2 is 1 (not 1.5).
// You may assume both numbers are positive and larger than 0.
// You can implement any algorithm, I recommend long division. If a natural number n is in R13 and a natural number m is in R14, then the complexity should be at most O(log(max(n, m))^2).

(INIT)
    @R14
    D=M
    @div
    M=D

    @R13
    D=M
    @num
    M=D

    @0
    D=A
    @R15
    M=D
    @result
    M=D

(ZEROCHECK)
// can't divide by 0
    @div
    D=M 
    @END
    D;JEQ 

(SMALLERCHECK)
    @num
    D=M
    @sub
    M=D

    @div
    D=M 
    @sub 
    D=M-D // sub = num - div -> should be > 0

    // if lower or equal, check if equal. 
    @INITAL
    D;JGT
    @EQUALCHECK
    D;JEQ
    @END
    D;JLT

(EQUALCHECK)
// if they are equal, than the answer is 1. (num-div=0-> num=div)
    @1
    D=A
    @result
    M=D
    @END
    0;JMP

(INITAL)
    @current
    M=1
	
(POWERS)	
	@num
	D=M 
    @sub
    M=D

	@div
	D=M
    @sub
    D=M-D // num - div

	@NEGATIVESUB
	D;JLT // num - div < 0 -> we reached below 0, should make smaller
	
	@div
	D=M<<
    // before we reach too many shifts, if we reached a negative(1 inside msb, we stop and start dividing)
	@DIVIDE
	D;JLE 
	
(UPGRADEPOWERS)
	@div
	M=M<< 
	@current
	M=M<< 
	
	@POWERS
	0;JMP
	
(NEGATIVESUB)
    @current
	M=M>> 
	@div
	M=M>>

// the dividing algorithm, with wanted powers:
(DIVIDE)
	@current
	D=M 
    // no powers inside, we stop:
	@END
	D;JEQ 
	
	// IF(dividend >= denom)
	@num
	D=M 
    @sub
    M=D

	@div
	D=M
    @sub
    D=M-D // sub = num - div

    // if positive - fits it.
	@CALCULATERESULT
	D;JGE 
	
    // else we make powers smaller
	@NEGATIVESUB
	D;JLT


(CALCULATERESULT)
	@current
	D=M 
	@result
	M=D+M 

    // we make number smaller, we need to fit div inside a smaller value afterwards.
	@div
	D=M 
	@num
	M = M-D 

	@NEGATIVESUB
	0;JMP
		
(END)
    @result
    D=M
    @R15
    M=D





    