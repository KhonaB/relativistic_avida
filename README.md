```
relativistic avidans are points with mass obeying relativistic mechanics
they execute avida assembly at constant speed in their frame of reference
avida assembly is inspired by Avida (github.com/devosoft/avida/)
notation is borrowed from the Avida wiki on GitHub
?BX? and ?CX? indicate default register that can be changed with a nop_ immediately following
the complement, or ~, of a nop is the following nop, looping at the end
#   inst    effect
a   nopa    do nothing, AX, IP, label a
b   nopb    do nothing, BX, RH, label b
c   nopc    do nothing, CX, WH, label c
d   ifne    execute next(+1) if ?BX? is not equal to ~ else skip
e   iflt    execute next(+1) if ?BX? is less than ~ else skip
f   pop     pop active stack to ?BX?
g   push    push ?BX? to active stack
h   swps    swap active stack
i   swpr    swap ?BX? with ~
j   hlv     halve ?BX?
k   dbl     double ?BX?
l   inc     increment ?BX?
m   dec     decrement ?BX?
n   add     add BX and CX and place in ?BX?
o   sub     subtract CX from BX and place in ?BX?
p   nand    nand BX and CX and place in ?BX?
q   io	    output ?BX? energy in a pulse from 2x radius and set that register to net (mass-)energy gain since last io
r   alloc   allocate max memory and load original memory size into AX if successful
s   div     split child at random separation/momentum, mem RH to WH, mass split with memory, preserving CoM/momentum
t   copy    copy from RH to WH and increment each, may error and place a random instruction at WH
u   find    find first ~(s) of label(s), with BX, CX, FH -> offset, length, location or 0, 0, IP+1
v   movh    move ?IP? to FH
w   jmph    move ?IP? by CX
x   geth    copy value of ?IP? to CX
y   iflbl   execute next(+n) if WH is immediately preceded by ~ of label(s) following
z   setf    move FH to ?CX?
```
