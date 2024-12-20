"""Autogenerated solution template, v2"""
__version__ = 2

from collections import defaultdict, namedtuple
from dataclasses import dataclass
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from lib.iterators import window

data = read_entire_input(2024,5)
test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".split("\n")

@dataclass
class RuleA():
    before: set
    after: set
    def __init__(self):
        self.before =set()
        self.after = set()

Rule = Tuple[int,int]
Rules = defaultdict[int, RuleA]
Ordering = List[int]

def parse(data: List[str]) -> Tuple[List[Rule], List[Ordering]]:
    a, b = "\n".join(data).split("\n\n")
    rules = a.split("\n")
    orderings = b.split("\n")
    rules = [tuple(map(int,row.split("|"))) for row in rules]
    orderings = [list(map(int,row.split(","))) for row in orderings]
    return rules, orderings

def process_rules(rules: List[Rule]) -> Rules:
    rule_dict: defaultdict[int, RuleA] = defaultdict(RuleA)
    for a, b in rules:
        rule_dict[a].before.add(b)
        rule_dict[b].after.add(a)
    return rule_dict

# def _satisfies_rule(rule: Rule, ordering: Ordering, pos: int) -> bool:
#     item = ordering[pos]
#     if item not in rule:
#         return True
#     pre = ordering[:pos]
#     post = ordering[pos+1:]  

def satisfies_rules(rules: Rules, ordering: Ordering) -> bool:
    for position, page in enumerate(ordering):
        before = ordering[:position]
        after = ordering[position+1:]
        rule = rules[page]
        
        if any(a in before for a in rule.before) or any(b in after for b in rule.after):
            # print(position, page)
            return False
    return True #ordering[len(ordering)//2]


#@solution_timer(2024,5,1)
def part_one(data: List[str], verbose=False):
    rules_list, orderings = parse(data)
    rules = process_rules(rules_list)
    tot = 0
    for ordering in orderings:
        if satisfies_rules(rules, ordering):
            tot += ordering[len(ordering)//2]
    return tot
    # return False

def correct_ordering(rules: Rules, ordering: Ordering) -> Ordering:
    new_ordering = [ordering[0]]
    for next_page in ordering[1:]:
        # print(f"examining page {next_page} into list {new_ordering}")
        # before the first page
        if next_page in rules[new_ordering[0]].after:
            # print(f"   according to rule {rules[new_ordering[0]]}, putting {next_page} at head")
            new_ordering.insert(0,next_page)
            continue
        if next_page in rules[new_ordering[-1]].before:
            # print(f"   according to rule {rules[new_ordering[0]]}, putting {next_page} at tail")
            new_ordering.append(next_page)
            continue
        # print("   sliding window approach")
        for pos, (a,b) in enumerate(window(new_ordering, 2)):
            # print(f"   ")
            if next_page in rules[a].before and next_page in rules[b].after:
                # print(f"        {a}: {rules[a]}")
                # print(f"        {b}: {rules[b]}")
                # print(f"   inserting {a}, <{next_page}>, {b}")
                new_ordering.insert(pos+1, next_page)
                break
    return new_ordering

#@solution_timer(2024,5,2)
def part_two(data: List[str], verbose=False):

    rules_list, orderings = parse(data)
    rules = process_rules(rules_list)
    tot = 0
    for ordering in orderings:
        if not satisfies_rules(rules, ordering):
            correct = correct_ordering(rules, ordering)
            tot += correct[len(correct)//2]
    return tot

if __name__ == "__main__":
    data = read_entire_input(2024,5)
    part_one(data)
    part_two(data)