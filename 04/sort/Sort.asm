// The program should sort the array starting at the address in R14 with length as specified in R15. Don't change these registers.
// The sort is in descending order - the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that R14 + R15 <= 16383. No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is at most C*O(N^2). I recommend bubble-sort.


(INIT)
    @R15
    D=M
    @length
    M=D
    
    // if the array is length 0 or less
    @END
    D;JLE

    @1
    D=A
    @comp
    M=D
    @length
    D=M
    @comp
    M=M-D
    D=M
    // if the array is length 1
    @END
    D;JEQ       

    @R14
    D=M
    @adrr
    M=D
    D=M // now the adress of the begining is inside D

    @i
    M=0
    @j
    M=0

    @GETVALUES
    0;JMP

    
(GETVALUES)
    @adrr
    D=M

    // set initial value
    @arrj0adrr // adress of arr[0]
    M=D
    @arrj1adrr // adress of arr[1]
    M=D+1

    // add current j to arr[0] to be arr[j]
    @j
    D=M
    @arrj0adrr
    M=M+D
    A=M
    D=M
    @value0
    M=D
    @comp // comp recieves the value of arr[j], if value[0]-value[1] > 0  we will swap
    M=D
    
    // add current j to arr[1] to be arr[j+1]
    @j
    D=M
    @arrj1adrr
    M=M+D
    A=M
    D=M
    @value1
    M=D
    
(CONDITION)
    @value1
    D=M
    @comp
    M=M-D // now it is value[0]-value[1]
    D=M

    @INNERLOOP
    D;JGE

(SWAP)
    @value0
    D=M
    @temp
    M=D // we save arr[j] in temp

    @value1
    D=M
    @arrj0adrr // we put arr[j+1] in arr[j]
    A=M
    M=D

    @temp
    D=M
    @arrj1adrr // and we put temp(arr[j]) in arr[j+1]
    A=M
    M=D 

(INNERLOOP)
    @j // we invest j->j+1
    M=M+1

    @length // we get n
    D=M
    @innerloopcounter // we set the counter of the loop to n
    M=D
    @i
    D=M

    @innerloopcounter
    M=M-D // M=n-i
    M=M-1 // M=n-i-1
    @j
    D=M
    @innerloopcounter
    M=D-M // M=j-(n-i-1) -> should be bigger than 0
    D=M

    @RESETINNER
    D;JGE
    @GETVALUES
    0;JMP
    
(RESETINNER)
    @j
    M=0
    @i
    M=M+1


(OUTERLOOP)
    @length
    D=M // this is n
    @outerloopcounter
    M=D-1 // M=n-1
    @i
    D=M // D=i
    @outerloopcounter
    M=D-M // M=i-(n-1) -> should be > 0 to continue
    D=M

    @END
    D;JGE
    @GETVALUES
    0;JMP

(END)


