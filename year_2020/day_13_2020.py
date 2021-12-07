from functools import reduce 
import math
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,13)
test="""939
7,13,x,x,59,x,31,19"""

def parse(data):
    time, busses = data
    time = int(time)
    busses = [int(bus) if bus != 'x' else None for bus in busses.split(',')]
    return time, busses

def compute_depature_time(earliest_leaving_time, active_busses):
    current_time = earliest_leaving_time
    while True:
        for bus_id in active_busses:
            if bus_id is None:
                continue
            if current_time % bus_id == 0:
                return current_time, bus_id
        current_time += 1

@solution_timer(2020,13,1)
def part_one(data):
    time, busses = parse(data)
    departure_time, bus_id = compute_depature_time(time, busses)
    return (departure_time-time)*bus_id

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

@solution_timer(2020,13,2)
def part_two(data):
    _, busses = parse(data)
    return solve(busses)


if __name__ == "__main__":
    data = read_entire_input(2020,13)
    part_one(data)
    part_two(data)