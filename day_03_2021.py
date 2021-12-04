from os import read
from adventofcode.util.input_helper import read_entire_input, read_input_by_line
from adventofcode.util.helpers import solution_timer

def compute_power_consumption(data):
    counter = [0] * len(data[0])
    for line in data: # read_input_by_line(2021,3):
        for i, digit in enumerate(line):
            # print(line)
            counter[i] += 1 if digit == '1' else -1
    gamma = ['1' if i > 1 else '0' for i in counter]
    epsilon = ['0' if i > 1 else '1' for i in counter]

    return int(''.join(gamma), base=2) * int(''.join(epsilon), base=2)

def compute_life_support(data):
    
    # OGR = read_entire_input(2021,3)
    OGR = [list(int(j) for j in i) for i in data]
    # print(OGR[:5])
    bit=0
    while len(OGR) > 1:
        mcb = 1 if sum(i[bit] for i in OGR) >= len(OGR)/2 else 0
        # print(f"examining bit {bit}: MCB is {mcb}")
        OGR = list(filter(lambda x: x[bit]==mcb, OGR))
        # print(f"   filtering, leaves {len(OGR)}")
        # print(OGR)
        # print(bit, len(OGR))
        bit += 1
    # print(OGR)

    # CO2S = read_entire_input(2021,3)
    CO2S = [list(int(j) for j in i) for i in data]

    bit=0
    while len(CO2S) > 1:
        lcb = 0 if sum(i[bit] for i in CO2S) >= len(CO2S)/2 else 1
        # print(f"examining bit {bit}: LCB is {lcb}")
        CO2S = list(filter(lambda x: x[bit]==lcb, CO2S))
        # print(f"   filtering, leaves {len(CO2S)}")
        # print(CO2S)
        bit += 1
    # print(CO2S)

    CO2 = ''.join([str(i) for i in CO2S[0]])
    O2 = ''.join([str(i) for i in OGR[0]])

    return int(''.join(O2), base=2) * int(''.join(CO2), base=2)

@solution_timer(2021,3,1)
def part_one(data):
    return compute_power_consumption(data)

@solution_timer(2021,3,2)
def part_two(data):
    return compute_life_support(data)

test_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

# compute_life_support(test_input.split("\n"))
if __name__ == '__main__':
    data = read_entire_input(2021,3)
    part_one(data)
    part_two(data)