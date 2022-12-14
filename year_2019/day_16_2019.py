from itertools import cycle
from typing import List, Any, Tuple
import math
from tqdm import trange
from framework.helpers import solution_timer, solution_profiler
from framework.input_helper import read_entire_input

data = read_entire_input(2019,16)

def parse(data: List[str]) -> Any:
    return [int(i) for i in data[0]]

def pattern(digit_number, cycle_length):
    PAT = [0,1,0,-1]
    return PAT[((digit_number+1) % (4 * cycle_length)) // cycle_length]   

def brute_force(digits, steps):
    PAT = [0,1,0,-1]
    for i in range(steps):
        output = []
        for cycle_length in range(1, len(digits)+1):
            v = 0
            for i, d in enumerate(digits):
                v += d * PAT[((i+1) % (4 * cycle_length)) // cycle_length]  #  pattern(i, cycle_length) having this function made it 3x slower
            output.append(abs(v)%10)
        digits = [i for i in output]
    return output

def better_approach(digits, steps,offset = 0):
    """Things to improve on:
    Avoid unnecessary multiplications and additions of zero
    """
    L = len(digits)
    digits = digits[offset:]
    PAT = [0,1,0,-1]
    for i in range(steps):
        output = []
        for cycle_length in range(offset,L): # Cycle length starting at 1 was useful before, but breaks my head now
            v = 0
            if cycle_length >= L//2:
                v = sum(digits[cycle_length-offset:])
            elif cycle_length >= L//3:
                v = sum(digits[cycle_length-offset:2*cycle_length+1-offset])
            elif cycle_length >= L//4:
                v = sum(digits[cycle_length-offset:2*cycle_length+1-offset]) - sum(digits[3*cycle_length+2-offset:])
            else:
                for i, d in enumerate(digits[cycle_length-offset:], start=cycle_length-offset): # Can only start from i, because 0 prior to this.
                    v += d * PAT[((i+1) % (4 * (cycle_length+1))) // (cycle_length+1)]  #  pattern(i, cycle_length) having this function made it 3x slower
            digits[cycle_length-offset] = abs(v) % 10
            #output.append(abs(v)%10)
        #digits = [i for i in output]
    return digits

# ARGH
def different_approach(digits, steps, offset):
    digits = digits[offset:]
    length = len(digits)
    for _ in range(steps):
        for i in range(length - 2, -1, -1):
            digits[i] = (digits[i] + digits[i + 1]) % 10
    return digits_to_int(digits[:8])

def digits_to_int(digits):
    return sum(10**i * d for i, d in enumerate(reversed(digits)))

@solution_timer(2019,16,1)
def part_one(data: List[str], verbose=False):
    digits = parse(data)
    output = better_approach(digits, 100)
    return digits_to_int(output[:8])

@solution_timer(2019,16,2)
def part_two(data: List[str], verbose=False):
    digits = parse(data) *10000
    offset = digits_to_int(digits[:7])
    return different_approach(digits, 100, offset)

if __name__ == "__main__":
    data = read_entire_input(2019,16)
    part_one(data)
    part_two(data)
