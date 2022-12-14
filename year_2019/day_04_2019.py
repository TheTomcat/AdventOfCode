from typing import Callable, List, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window

data = read_entire_input(2019,4)

def parse(data: List[str]) -> Tuple[int, int]:
    return [int(i) for i in data[0].split("-")]

def int_to_digit_list(input: int) -> List[int]:
    return [int(i) for i in list(str(input))]
def digit_list_to_int(input: List[int]) -> int:
    return sum(10**(len(input)-1-i)*digit for i, digit in enumerate(input))

def find_next_monotonic_password(digits):
    for i, (a,b) in enumerate(window(digits)):
        if a <= b:
            continue
        else:
            break
    for j in range(i,len(digits)):
        digits[j] = digits[i]
    return digits

def brute_check(start: int, end: int, validator: Callable):
    count = 0
    for password in range(start, end+1):
        digits = int_to_digit_list(password)
        if validator(digits):
            count += 1
    return count

def increment(digits, d_pos=None):
    ones_digit = len(digits)-1
    if d_pos is None:
        d_pos = ones_digit
    if d_pos < 0: # trying to increment numbers that don't exist
        return False   
    digits[d_pos] += 1 # try to increment it
    if digits[d_pos] > 9: # if you've gone too far, 
        return increment(digits, d_pos-1) # increment the next digit down
    for digit in range(d_pos+1, len(digits)):
        digits[digit] = digits[d_pos]
        digits[digit] = digits[d_pos]
    return digits

def smart_check(start: int, end: int, validator: Callable):
    candidates = []
    digits = find_next_monotonic_password(int_to_digit_list(start))
    while digits:
        if validator(digits): # at least one digit is repeated
            num = digit_list_to_int(digits)
            if num > end:
                return candidates
            candidates.append(num)
        digits = increment(digits)
    return candidates

def has_repeated_digits(digits):
    return len(set(digits)) < len(digits)

def has_exactly_double_digits(digits: List[int]):
    # The digits that are repeated MUST be next to each other
    for i in range(10):
        if digits.count(i) == 2:
            return True
def is_monotonic(digits):
    return all(a <= b for a,b in window(digits))

def is_part_one_password(digits: List[int]) -> bool:
    return is_monotonic(digits) and has_repeated_digits(digits)

@solution_timer(2019,4,1)
def part_one(data: List[str], verbose=False):
    low, high = parse(data)
    return len(smart_check(low, high, has_repeated_digits)) # 3ms -> No need to check for monotonicity as the iterator does that already
    #return brute_check(low, high, is_part_one_password) # 950ms

@solution_timer(2019,4,2)
def part_two(data: List[str], verbose=False):
    low, high = parse(data)
    return len(smart_check(low, high, has_exactly_double_digits)) # 3ms

if __name__ == "__main__":
    data = read_entire_input(2019,4)
    part_one(data)
    part_two(data)