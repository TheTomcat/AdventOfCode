from itertools import islice
from adventofcode.util.input_helper import read_entire_input

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

with open("2021/1/input.txt", "r") as f:
    old_num=0
    inc_count=-1
    for line in f:
        new_num = int(line)
        if new_num > old_num:
            inc_count += 1
        old_num = new_num

print(inc_count)

with open("2021/1/input.txt", "r") as f:
    inc_count = 0
    for a,b,c,d in window(f, 4):
        if int(a) < int(d):
            inc_count += 1

print(inc_count)