from functools import lru_cache
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from lib.graph.Graph import Graph

data = read_entire_input(2022,21)
test = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".split("\n")

def parse(data: List[str]) -> Any:
    instructions = {}
    for monkey in data:
        name, action = monkey.split(": ")
        if action.isdigit():
            payload = int(action)
        else:
            payload = (action[5], action[:4], action[7:])
        instructions[name] = payload
    return instructions

def evaluate(instructions, node='root', is_part_two=False, humn=0):
    if node == 'humn' and is_part_two:
        return humn
    if isinstance(instructions[node], int):
        return instructions[node]
    else:
        op, a, b = instructions[node]
        if node == 'root' and is_part_two:
            return evaluate(instructions, a, is_part_two, humn), evaluate(instructions, b, is_part_two, humn)
        match op:
            case '+':
                return evaluate(instructions, a, is_part_two, humn) + evaluate(instructions, b, is_part_two, humn)
            case '-':
                return evaluate(instructions, a, is_part_two, humn) - evaluate(instructions, b, is_part_two, humn)
            case '*':
                return evaluate(instructions, a, is_part_two, humn) * evaluate(instructions, b, is_part_two, humn)
            case '/':
                return evaluate(instructions, a, is_part_two, humn) / evaluate(instructions, b, is_part_two, humn)

def solver(f, x0, tol=0.01):
    guess = x0
    y = f(guess)
    while abs(y) > tol:
        m = (y - f(guess+1))
        guess = guess + int(y/m)
        y = f(guess)
        # print(guess, y)
        # input()
    return guess

@solution_timer(2022,21,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    return evaluate(instructions)

@solution_timer(2022,21,2)
def part_two(data: List[str], verbose=False):
    instructions = parse(data)
    d = lambda p: p[1]-p[0]
    f = lambda humn: d(evaluate(instructions, 'root', is_part_two=True, humn=humn))
    return solver(f, 300)

if __name__ == "__main__":
    data = read_entire_input(2022,21)
    part_one(data)
    part_two(data)