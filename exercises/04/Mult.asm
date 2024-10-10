// Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])
// Usage: Before executing, put two values in R0 and R1.

//set sum to 0
@sum
M=0

//set y=RAM[1]
@R1
D=M
@y
M=D

//jump to negative loop if y < 0
@NEGATIVE
D;JLT

//loop for positive y
(POSITIVE)
@STOP
D;JEQ
@R0
D=M
@sum
M=D+M
@y
M=M-1
D=M
@POSITIVE
0;JMP

//loop for negative y
(NEGATIVE)
@STOP
D;JEQ
@R0
D=M
@sum
M=M-D
@y
M=M+1
D=M
@NEGATIVE
0;JMP


(STOP)
@sum
D=M
@R2
M=D

(END)
@END
0;JMP

