import math

def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    time, busses = text.split('\n')
    time = int(time)
    busses = [int(bus) if bus != 'x' else None for bus in busses.split(',')]
    return time, busses

def compute(earliest_leaving_time, active_busses):
    current_time = earliest_leaving_time
    while True:
        for bus_id in active_busses:
            if bus_id is None:
                continue
            if current_time % bus_id == 0:
                return current_time, bus_id
        current_time += 1


test = """939
7,13,x,x,59,x,31,19"""
earliest_leaving_time_test, busses_test = process(test)

time_depart, bus_id = compute(earliest_leaving_time_test, busses_test)
print(time_depart, bus_id, (time_depart-earliest_leaving_time_test)*bus_id)


earliest_leaving_time, busses = process(read_input(13))
time_depart, bus_id = compute(earliest_leaving_time, busses)
print(time_depart, bus_id, (time_depart-earliest_leaving_time)*bus_id)

# bus_id * n = t + t_offset for all busses
# t = bus_id * n - t_offset
# t === - t_offset (mod bus_id)

def lcm(args):
    lcm = 1
    for i in args:
        if i is None:
            continue
        lcm = lcm*i//math.gcd(lcm, i)
    return lcm

from functools import reduce
def chinese_remainder(modulos, remainders):
    tot = 0
    prod = reduce(lambda a, b: a*b, modulos)
    for n_i, a_i in zip(modulos, remainders):
        p = prod // n_i
        tot += a_i * mul_inv(p, n_i) * p
    return tot % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def solve(active_busses):
    remainders = [-i for i,v in enumerate(active_busses) if v is not None]
    modulos = [v for v in active_busses if v is not None]
    return chinese_remainder(modulos, remainders)
    

print(solve(busses))
print(solve(busses_test))