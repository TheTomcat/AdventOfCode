from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window
from framework.console import console

from functools import cmp_to_key

data = read_entire_input(2022,13)
test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".split("\n")

def parse(data: List[str]) -> Any:
    v = iter(data)
    packets = []
    while True:
        a = next(v)
        b = next(v)
        packets.append((eval(a), eval(b)))
        try:
            next(v)
        except StopIteration:
            break
    return packets

def compare(left, right):
    match left, right:
        case int(), int():
            return left - right
        case list(), list():
            for l,r in zip(left, right):
                if (e := compare(l,r)) != 0:
                    return e
            return len(left) - len(right)
        case list(), int():
            return compare(left,[right])
        case int(), list():
            return compare([left],right)

@solution_timer(2022,13,1)
def part_one(data: List[str], verbose=False):
    packets = parse(data)
    return sum([i+1 for i, (left, right) in enumerate(packets) if compare(left, right) < 0])

@solution_timer(2022,13,2)
def part_two(data: List[str], verbose=False):
    packets = parse(data)
    new_packets = sorted([packet for pair in packets for packet in pair] + [[[2]]] + [[[6]]], key=cmp_to_key(compare))
    if verbose:
        console.print('\n'.join(f'{index+1:03}: {"[red]" if packet in [[[2]],[[6]]] else ""}{packet}{"[/red]" if packet in [[[2]],[[6]]] else ""}' for index, packet in enumerate(new_packets)))
    return (new_packets.index([[2]]) + 1) * (new_packets.index([[6]]) + 1)

if __name__ == "__main__":
    data = read_entire_input(2022,13)
    part_one(data)
    part_two(data)