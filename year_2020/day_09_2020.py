from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from lib.iterators import window

data = read_entire_input(2020,9)

def parse(data):
    return [int(i) for i in data]

def find_fault(bits):
    for i in range(len(bits)-25):
        tot = bits[i+25]
        for num in bits[i:i+25]:
            if tot - num in bits[i:i+25]:
                break
        else:
            return tot

def break_cipher(bits):
    tot = find_fault(bits)
    for lower in range(len(bits)):
        for length in range(1, len(bits)-lower):
            add = sum(bits[lower:lower+length])
            if add > tot:
                break
            elif add == tot:
                return min(bits[lower:lower+length]) + max(bits[lower:lower+length])
            
@solution_timer(2020,9,1)
def part_one(data, verbose=False):
    bits = parse(data)
    return find_fault(bits)

@solution_timer(2020,9,2)
def part_two(data, verbose=False):
    bits = parse(data)
    return break_cipher(bits)

if __name__ == "__main__":
    data = read_entire_input(2020,9)
    part_one(data)
    part_two(data)