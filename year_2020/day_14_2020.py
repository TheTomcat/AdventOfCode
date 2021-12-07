from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,14)

def parse(data):
    commands = []
    for line in data:
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

@solution_timer(2020,14,1)
def part_one(data):
    commands = parse(data)
    mem = run(commands)
    return sumup(mem)


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

@solution_timer(2020,14,2)
def part_two(data):
    commands = parse(data)
    mem = run2(commands)
    return sumup(mem)


if __name__ == "__main__":
    data = read_entire_input(2020,14)
    part_one(data)
    part_two(data)