from typing import List
from operator import add, mul
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,18)

def parse(data) -> List[List[str]]:
    return [tokenise(element) for element in data]

def tokenise(exp: str) -> List[str]:
    exp = exp.replace(" ","")
    output = []
    numeric_token = ''
    for character in exp:
        if character in '+*()':
            if numeric_token:
                output.append(int(numeric_token))
            output.append(character)
            numeric_token = ''
        else:
            numeric_token += character
    if numeric_token:
        output.append(int(numeric_token))
    return output


def evaluate_bracketed_expression(exp, left_to_right=True):
    i=0
    while True:
        if ")" in exp:
            i_close = exp.index(")",i)
            for index in range(i_close,-1,-1):
                if exp[index] == "(":
                    i_open = index
                    break
            if left_to_right:
                exp[i_open:i_close+1] = [evaluate_simple_expression_left_to_rigt(exp[i_open+1:i_close])]
            else:
                exp[i_open:i_close+1] = [evaluate_simple_expression_reverse(exp[i_open+1:i_close])]
            i=i_open
        else:
            if left_to_right:
                return evaluate_simple_expression_left_to_rigt(exp)
            else:
                return evaluate_simple_expression_reverse(exp)
    
def evaluate_simple_expression_left_to_rigt(exp):
    if len(exp)==1:
        return exp[0]
    if len(exp) == 0:
        return
    if '(' in exp:
        print(exp)
        raise ValueError("Cannot parse '(' in simple expression")
    
    n1 = int(exp[0])
    op = exp[1]
    n2 = int(exp[2])
    res = opl[op](n1,n2)
    exp = [res] + exp[3:]
    return evaluate_simple_expression_left_to_rigt(exp)

def evaluate_simple_expression_reverse(exp):
    if len(exp)==1:
        return exp[0]
    if len(exp) == 0:
        return
    if '(' in exp:
        print(exp)
        raise ValueError("Cannot parse '(' in simple expression")
    if "+" in exp:
        i = exp.index("+")
        n1 = int(exp[i-1])
        n2 = int(exp[i+1])
        op = "+"
        res = opl[op](n1,n2)
        exp = exp[:i-1] + [res] + exp[i+2:]
    else:
        n1 = int(exp[0])
        op = exp[1]
        n2 = int(exp[2])
        res = opl[op](n1,n2)
        exp = [res] + exp[3:]
    return evaluate_simple_expression_reverse(exp)

opl = {"+":add,
       "*":mul}

@solution_timer(2020,18,1)
def part_one(data):
    tokens = parse(data)
    return sum(evaluate_bracketed_expression(i) for i in tokens)


@solution_timer(2020,18,2)
def part_two(data):
    tokens = parse(data)
    return sum(evaluate_bracketed_expression(i, left_to_right=False) for i in tokens)

if __name__ == "__main__":
    data = read_entire_input(2020,18)
    part_one(data)
    part_two(data)