import re
from collections import defaultdict

from util.helpers import solution_timer
from util.input_helper import read_entire_input

recnt = re.compile(r'(\d)+ ([\w ]*)(bag)s?')

data = read_entire_input(2020,7)

def parse(data):
    ruledict = {}
    for rule in data:
        pre,post = rule.split(' bags contain ')
        ruledict[pre.lower()] = []
        for num, bag, _ in recnt.findall(post):
            ruledict[pre.lower().strip()].append((num, bag.lower().strip()))
    return ruledict

def inverse_rules(rules):
    output = defaultdict(list)
    for pre in rules:
        for num, bag in rules[pre]:
            output[bag].append(pre)
    return output

def find_parent_bags(target, reversed_rule_dict, traversed=None):
    if traversed is None:
        traversed=[]
    parents = reversed_rule_dict[target]
    count = 0
    for parent in parents:
        if parent in traversed:
            continue
        traversed.append(parent)
        count += 1
        count +=  find_parent_bags(parent, reversed_rule_dict, traversed)
    return count

def count_bags(target, rule_dict):
    bags = 0
    for num, bag in rule_dict[target]:
        #print(rule_dict[target])
        bags += int(num) * (1+count_bags(bag, rule_dict))
    return bags

@solution_timer(2020,7,1)
def part_one(data):
    rules = parse(data)
    return find_parent_bags("shiny gold", inverse_rules(rules))

@solution_timer(2020,7,2)
def part_two(data):
    rules = parse(data)
    return count_bags("shiny gold", rules)
    # return False

if __name__ == "__main__":
    data = read_entire_input(2020,7)
    part_one(data)
    part_two(data)