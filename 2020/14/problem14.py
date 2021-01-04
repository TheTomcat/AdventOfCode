def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    lines = text.split('\n')
    commands = []
    for line in lines:
        if line.startswith('mem'):
            cmd, val = line.split(' = ')
            cmd = cmd.split('[')[-1][:-1]
            commands.append(('mem',(int(cmd),int(val))))
        elif line.startswith('mask'):
            cmd, val = line.split(' = ')
            commands.append(('mask', val))
    return commands

def do(memory, command, args):
    if command == 'mem':
        addr, val = args
        mask = memory['mask']
        memory[addr] = write(mask, val)
    elif command == 'mask':
        mask = args
        memory['mask'] = mask
    return memory

def write(mask, val):
    sval = f"{val:036b}"
    o = ''
    for m,v in zip(mask, sval):
        if m == "X":
            o += v
        else:
            o += m
    return int(o,2)

def run(commands):
    mem = {'mask':""}
    for command, arg in commands:
        mem = do(mem,command,arg)
    return mem

def sumup(mem):
    tot = 0
    for key in mem:
        if key == "mask":
            continue
        tot += mem[key]
    return tot
    

commands = process(read_input(14))

mem = run(commands)
print(sumup(mem))

def do2(memory, command, args):
    if command == 'mem':
        addr, val = args
        mask = memory['mask']
        memory = write2(memory, mask, addr, val)
    elif command == 'mask':
        mask = args
        memory['mask'] = mask
    return memory

def write2(memory, mask, addr, val):
    for addr in iterate_masks(mask, addr):
        memory[addr] = val
    return memory

def run2(commands):
    mem = {'mask':""}
    for command, arg in commands:
        mem = do2(mem,command,arg)
    return mem

def iterate_masks(mask, addr):
    num_Xs = mask.count("X")
    for i in range(2**num_Xs):
        yield combine(mask, i, addr)

def combine(mask, digits, addr):
    addr = f'{addr:036b}'
    num_Xs = mask.count("X")
    fstr = f'0{num_Xs}b'
    bindigits = f'{digits:{fstr}}'
    newmask = ''
    i=0
    for mdig, adig in zip(mask, addr):
        if mdig == "X":
            newmask += bindigits[i]
            i+=1
        elif mdig == "0":
            newmask += adig
        else:
            newmask += "1"
    return newmask

# test = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0"""

# commands = process(test)
mem = run2(commands)
print(sumup(mem))