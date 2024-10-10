// Computes R0 = 2 + 3  (R0 refers to RAM[0])

(LOOP)
@scrn
M=0

@8192
D=A
@i
M=D

@SCREEN
D=A
@addr
M=D

@KBD
D=M
@SET
D;JGT
@DRAW
0;JMP

(SET)
@scrn
M=-1

(DRAW)
@scrn
D=M
@addr
A=M
M=D
@addr
M=M+1
@i
M=M-1
D=M
@LOOP
D;JEQ
@DRAW
0;JMP

(END)
@END
0;JMP