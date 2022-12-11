from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

import re
from math import prod, lcm

data = read_entire_input(2022,11)
test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".split("\n")

def parse(data: List[str]) -> Any:
    regex = r'Monkey (\d+):\n\s*Starting items: (.+)\n\s*Operation: new = (.*)\n\s*Test: divisible by (\d+)\n\s*If true: throw to monkey (\d+)\n\s+If false: throw to monkey (\d+)'
    monkeys = {}
    for match in re.finditer(regex, '\n'.join(data)):
        index, items, operation, condition, true, false = match.groups()
        m = Monkey(items = [int(i) for i in items.split(", ")],
                   operation = oper(operation),
                   test = int(condition),
                   on_true = int(true),
                   on_false = int(false))
        monkeys[int(index)] = m
    return monkeys
    
def oper(operation):
    if operation.count('old') == 2 and operation.count('*')==1:
        return lambda x: x*x
    if operation.count(" + ") == 1:
        v = int(operation[6:])
        return lambda x: x + v
    if operation.count(" * ") == 1:
        v = int(operation[6:])
        return lambda x: x*v

class Monkey:
    def __init__(self, items, operation, test, on_true, on_false):
        self.items = items
        self.operation = operation
        self.test = test
        self.on_true = on_true
        self.on_false = on_false
        self.inspections = 0
    def take_turn(self, monkeys, part_one=True, worry_reducer=1):
        while self.items:
            item = self.items.pop(0)
            #print(f"  Monkey inspects an item with a worry level of {item}")
            self.inspections += 1
            item = self.operation(item)
            #print(f"    Worry level is modified to {item}")
            if part_one:
                item = item // 3
            else:
                item = item % worry_reducer
            #print(f"    Monkey gets bored with item. Worry level is divided by 3 to {item}")
            if item % int(self.test) == 0:
                #print(f"    Current worry level is divisible by {self.test}")
                monkeys[self.on_true].accept(item)
                #print(f"    Item with worry level {item} is thrown to monkey {self.on_true}.")
            else:
                #print(f"    Current worry level is not divisible by {self.test}")
                monkeys[self.on_false].accept(item)
                #print(f"    Item with worry level {item} is thrown to monkey {self.on_false}.")
    def accept(self, item):
        self.items.append(item)

@solution_timer(2022,11,1)
def part_one(data: List[str]):
    monkeys = parse(data)
    for i in range(20):
        for index, monkey in monkeys.items():
            monkey.take_turn(monkeys)
    return prod(sorted([i.inspections for i in monkeys.values()], reverse=True)[:2])

@solution_timer(2022,11,2)
def part_two(data: List[str]):
    monkeys = parse(data)
    worry_reducer = lcm(*(monkey.test for monkey in monkeys.values()))
    for i in range(10000):
        for index, monkey in monkeys.items():
            monkey.take_turn(monkeys, part_one=False, worry_reducer=worry_reducer)
        # print(f"== After round {i+1} ==")
        # for index, monkey in monkeys.items():
        #     print(f"Monkey {index} inspected items {monkey.inspections} times.")
        # input()
    return prod(sorted([i.inspections for i in monkeys.values()], reverse=True)[:2])

if __name__ == "__main__":
    data = read_entire_input(2022,11)
    part_one(data)
    part_two(data)