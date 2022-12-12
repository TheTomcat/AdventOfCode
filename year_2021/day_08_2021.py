from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,8)

def parse(data: List[str]) -> Any:
    input_digits = []
    output_digits = []
    for row in data:
        a,b = row.split(" | ")
        input_digits.append([set(i) for i in a.split(" ")])
        output_digits.append([set(i) for i in b.split(" ")])
    return input_digits, output_digits

@solution_timer(2021,8,1)
def part_one(data: List[str], verbose=False):
    _, output_digits = parse(data)
    count = 0
    for entry in output_digits:
        for digit in entry:
            if len(digit) in [2,3,4,7]:
                count += 1
    return count

def decode_signal(input_signal: List[set], output_signal: List[set]):
    # pre-processing
    output = []
    zero = one = two = three = four = five = six = seven = eight = nine = None
    # Rules: 1 intersect (5 segment) -> 
    one = next(filter(lambda x: len(x) == 2, input_signal+output_signal), None)
    four = next(filter(lambda x: len(x) == 4, input_signal+output_signal), None)
    seven = next(filter(lambda x: len(x) == 3, input_signal+output_signal), None)
    eight = next(filter(lambda x: len(x) == 7, input_signal+output_signal), None)
    s_five = list(filter(lambda x: len(x) == 5, input_signal+output_signal)) # 2,3,5
    s_six = list(filter(lambda x: len(x) == 6, input_signal+output_signal))  # 0,6,9

    if one is not None:
        three = next(filter(lambda x: one.intersection(x) == one, s_five), None) # ONE intersecting with a 5-segment 
        five = next(filter(lambda x: one.union(x) in s_six, s_five), None) # ONE unioning with a 5-segment producing a 6-segment = 5
        six = next(filter(lambda x: len(one.union(x))==7, s_six), None) # one union six = eight

    if seven is not None:
        if three is None:
            three = next(filter(lambda x: seven.union(x)==x, s_five), None) # seven union three = three
        nine = next(filter(lambda x: seven.intersection(x)==seven, s_six), None)

    if four is not None:
        two = next(filter(lambda x: len(four.union(x))==7, s_five), None)
        if nine is not None:
            nine = next(filter(lambda x: four.union(x)==x, s_six), None)
    
        d_segment = {'a','b','c','d','e','f','g'}
        for d in s_five:
            d_segment.intersection_update(d)
        d_segment.intersection_update(four)
        zero = next(filter(lambda x: len(d_segment.union(x))==7, s_six), None)
    if None in [zero, one, two, three, four, five, six, seven, eight, nine]:
        raise ValueError("Need more rules")
    return  [zero, one, two, three, four, five, six, seven, eight, nine]

def read_output(input_signal: List[set], output_signal: List[set]) -> int:
    digits = decode_signal(input_signal, output_signal)
    output = []
    for digit in output_signal:
        output.append(digits.index(digit))
    return 1000*output[0] + 100*output[1] + 10*output[2] + output[3]

@solution_timer(2021,8,2)
def part_two(data: List[str], verbose=False):
    inputs, outputs = parse(data)
    total = 0
    for input_signal, output_signal in zip(inputs, outputs):
        total += read_output(input_signal, output_signal)
    return total

if __name__ == "__main__":
    data = read_entire_input(2021,8)
    part_one(data)
    part_two(data)