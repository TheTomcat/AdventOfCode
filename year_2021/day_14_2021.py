from itertools import count
from typing import DefaultDict, Dict, List, Any, Tuple
from collections import Counter, defaultdict
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from lib.iterators import window

data = read_entire_input(2021,14)
test = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split('\n')

def parse(data: List[str]) -> Any:
    template = list(data[0])
    rules = {}
    for rule in data[2:]:
        a,b = rule.split(" -> ")
        rules[a] = b
    return template, rules

def polymerise_brute_force(template, rules):
    output = ''
    for a,b in window(template):
        if a+b in rules:
            output += a + rules[a+b] 
        else:
            output += a
    return output+b

def prepare_template(template):
    "Take the template and look at each pair of elements, tallying them as we go"
    polymer = defaultdict(int)
    for a,b in window(template):
        polymer[a+b] += 1
    return polymer

def process_rules(template_dict: DefaultDict, rules: Dict):
    """Take the template dict from prepare_template and apply each rule:
    For the rule AB -> C
    Split the key AB into AC and CB
    this happens as many times as the original key appears
    """
    new_polymer = defaultdict(int)
    for rule, replacement in rules.items():
        vala = rule[0] + replacement
        valb = replacement + rule[1]
        new_polymer[vala] += template_dict[rule]
        new_polymer[valb] += template_dict[rule]
        del template_dict[rule]
    new_polymer.update(template_dict)
    return new_polymer

def count_elements(polymer_dict: DefaultDict):
    "Count each element from pairs in the polymer dict (counts twice, except for the first and last element which is invariant and only counted once)"
    elements = defaultdict(int)
    for element, amt in polymer_dict.items():
        elements[element[0]] += amt
        elements[element[1]] += amt
    return elements

def rapid_polymerise(template, rules, steps):
    "Rapid polymerisation algorithm"
    first_element = template[0]
    last_element = template[-1]
    polymer = prepare_template(template)
    for _ in range(steps):
        polymer = process_rules(polymer, rules)
    elements = count_elements(polymer)
    elements[first_element] += 1 # Remember to add the first and last elements
    elements[last_element] += 1
    return elements

@solution_timer(2021,14,1)
def part_one(data: List[str], verbose=False):
    template, rules = parse(data)
    polymer = rapid_polymerise(template, rules, 10)
    return (max(polymer.values()) - min(polymer.values()))/2
    # template, rules = parse(data)
    # for step in range(10):
    #     template = polymerise_brute_force(template, rules)
    # c = Counter(template)
    # return max(c.values()) - min(c.values())

@solution_timer(2021,14,2)
def part_two(data: List[str], verbose=False):
    template, rules = parse(data)
    polymer = rapid_polymerise(template, rules, 40)
    return (max(polymer.values()) - min(polymer.values()))/2

if __name__ == "__main__":
    data = read_entire_input(2021,14)
    part_one(data)
    part_two(data)