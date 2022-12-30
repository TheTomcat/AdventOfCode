from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2022,25)
test = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""".split("\n")

digits = {'=':-2, '-':-1, '0':0, '1':1, '2':2}
rdigits = {val: key for key, val in digits.items()}

def parse(data: List[str]) -> Any:
    return data

def dec_to_balanced_quinary(decimal: int) -> str:
    quin = dec_to_quinary(decimal)
    bal_quin = [0]*(len(quin)+1)
    carry = 0
    for i, digit in enumerate(quin[:-1]):
        digit += carry
        if digit > 2:
            bal_quin[i] = digit - 5
            bal_quin[i+1] += 1
            carry = 1
        else:
            bal_quin[i] = digit
            carry = 0
    return bal_quin

def dec_to_quinary(decimal: int) -> list:
    remainder = 0
    factor = decimal
    output = []
    while factor or remainder:
        factor, remainder = divmod(factor,5)
        output.append(remainder)
    return output

def balanced_quinary_to_decimal(quinary: str) -> int:
    return sum(5**i * digits[dec] for i, dec in enumerate(reversed(quinary)))

@solution_timer(2022,25,1)
def part_one(data: List[str], verbose=False):
    numbers = parse(data)
    output = [0]*30
    for number in numbers:
        for i, digit in enumerate(reversed(number)):
            output[i] += digits[digit]
    total = sum(digit * 5 ** i for i, digit in enumerate(output))
    return ''.join(rdigits[digit] for digit in reversed(dec_to_balanced_quinary(total))).lstrip('0')

@solution_timer(2022,25,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2022,25)
    part_one(data)
    part_two(data)