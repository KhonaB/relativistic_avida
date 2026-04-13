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

def ifnop(cpu, nop = 'bx'):
    '''check, return, and skip nop at ip+1'''
    #Reselect register and advance IP if nop specifier next
    nxt = (cpu.ip + 1) % len(cpu.mem)
    if cpu.mem[nxt] in nops:
        nop = f'{cpu.mem[nxt]}x'
        cpu.ip = nxt
    return nop

def ifcmp(cpu, cmp):
    '''execute next(+1) if ?BX? is <cmp> ~ else skip'''
    #Get ?BX?
    nop = ifnop(cpu)
    
    #Test <op> and advance IP accordingly
    if not cmp(getattr(cpu, nop), getattr(cpu, get_cmp(nop))):
        cpu.ip = (cpu.ip + 1) % len(cpu.mem)

def ifne(cpu):
    '''execute next(+1) if ?BX? is not equal to ~ else skip'''
    #Defer to ifcmp
    ifcmp(cpu, int.__ne__)

def iflt(cpu):
    '''execute next(+1) if ?BX? is less than ~ else skip'''
    #Defer to ifcmp
    ifcmp(cpu, int.__lt__)

def pop(cpu):
    '''pop active stack to ?BX?'''
    #Get ?BX? and active stack
    nop = ifnop(cpu)
    stk = cpu.stx[cpu.act]

    #Load 0 to ?BX? if stack empty else pop stack
    if len(stk) == 0:
        setattr(cpu, nop, 0)
    else:
        setattr(cpu, nop, stk.pop())

def push(cpu):
    '''push ?BX? to active stack'''
    #Get ?BX? and active stack
    nop = ifnop(cpu)
    stk = cpu.stx[cpu.act]

    #Push ?BX? to stack
    stk.append(getattr(cpu, nop))

#Translates from a gene to an executable instruction
GENOME={
        'a': nopa,
        'b': nopb,
        'c': nopc,
        'd': ifne,
        'e': iflt,
        'f': pop,
        'g': push,
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
        #Stacks and active stack
        self.stx = ([], [])
        self.act = 0
        #Memory
        self.mem = mem

    def get_hd(self, nop):
        '''Get head corresponding to nop'''
        match nop:
            case 'a':
                return 'ip'
            case 'b':
                return 'rh'
            case 'c':
                return 'wh'
            case 'd':
                return 'fh'

    def get_cmp(self, nop):
        '''Get complement of nop'''
        match nop:
            case 'ax':
                return 'bx'
            case 'bx':
                return 'cx'
            case 'cx':
                return 'ax'

    def exec(self, debug = False):
        '''Execute next instruction'''
        
        #Execute function corresponding to mem[ip]
        GENOME[self.mem[self.ip]](self)

        #Move on to next instruction by default
        self.ip = (self.ip + 1) % len(self.mem)

        #Dump state if debug flag
        if debug:
            print(vars(self))
