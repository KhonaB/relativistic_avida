nops = ('a', 'b', 'c')

def nopa(cpu):
    '''do nothing, AX, IP, label a'''
    pass

def nopb(cpu):
    '''do nothing, BX, RH, label b'''
    pass

def nopc(cpu):
    '''do nothing, CX, WH, label c'''
    pass

def ifcmp(cpu, cmp):
    '''execute next(+1) if ?BX? is <cmp> ~ else skip'''
    
    #Default register
    nop = 'b'

    #Reselect register and advance IP if nop specifier next
    nxt = (cpu.ip + 1) % len(cpu.mem)
    if cpu.mem[nxt] in nops:
        nop = cpu.mem[nxt]
        cpu.ip = nxt

    #Test <op> and advance IP accordingly
    if not cmp(cpu.get_rx(nop), cpu.get_rx(nop, True)):
        cpu.ip = (cpu.ip + 1) % len(cpu.mem)

def ifne(cpu):
    '''execute next(+1) if ?BX? is not equal to ~ else skip'''
    #defer to ifcmp
    ifcmp(cpu, int.__ne__)

def iflt(cpu):
    '''execute next(+1) if ?BX? is less than ~ else skip'''
    #defer to ifcmp
    ifcmp(cpu, int.__lt__)

#Translates from a gene to an executable instruction
GENOME={
        'a': nopa,
        'b': nopb,
        'c': nopc,
        'd': ifne,
        'e': iflt,
#        'f': pop,
#        'g': push,
#        'h': swps,
#        'i': swpr,
#        'j': hlv,
#        'k': dbl,
#        'l': inc,
#        'm': dec,
#        'n': add,
#        'o': sub,
#        'p': nand,
#        'q': io,
#        'r': alloc,
#        's': div,
#        't': copy,
#        'u': find,
#        'v': movh,
#        'w': jmph,
#        'x': geth,
#        'y': iflbl,
#        'z': setf
}

class cpu:
    '''Acts as the cpu of an RA'''
    def __init__(self, mem):
        #Instruction pointer
        self.ip = 0
        #Read, write, and flow heads
        self.rh = 0
        self.wh = 0
        self.fh = 0
        #Registers
        self.ax = 0
        self.bx = 0
        self.cx = 0
        #Stacks
        self.stx = ([], [])
        #Memory
        self.mem = mem

    def get_hd(self, nop):
        '''Get head corresponding to nop'''
        match nop:
            case 'a':
                return self.ip
            case 'b':
                return self.rh
            case 'c':
                return self.wh

    def get_rx(self, nop, cmpl=False):
        '''Get register (or complement) corresponding to nop'''
        match nop:
            case 'a':
                return self.ax if not cmpl else self.bx
            case 'b':
                return self.bx if not cmpl else self.cx
            case 'c':
                return self.cx if not cmpl else self.ax

    def exec(self):
        '''Execute next instruction'''
        
        #Execute function corresponding to mem[ip]
        GENOME[self.mem[self.ip]](self)

        #Move on to next instruction by default
        self.ip = (self.ip + 1) % len(self.mem)
