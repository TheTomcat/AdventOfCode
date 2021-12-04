import re
from collections import defaultdict

recnt = re.compile(r'(\d)+ ([\w ]*)(bag)s?')

def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def compile_rule_dict(data):
    ruledict = {}
    for rule in data.split('\n'):
        pre,post = rule.split(' bags contain ')
        ruledict[pre.lower()] = []
        for num, bag, _ in recnt.findall(post):
            ruledict[pre.lower().strip()].append((num, bag.lower().strip()))
    return ruledict

def reverse_rule_dict(rule_dict):
    output = defaultdict(list)
    for pre in rule_dict:
        for num, bag in rule_dict[pre]:
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

test="""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

test2="""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

print(compile_rule_dict(test))
print(reverse_rule_dict(compile_rule_dict(test)))
print(find_parent_bags("shiny gold", reverse_rule_dict(compile_rule_dict(test))))
data = read_input(7)
print(find_parent_bags("shiny gold", reverse_rule_dict(compile_rule_dict(data))))

print(count_bags("shiny gold", compile_rule_dict(test2)))
print(count_bags("shiny gold", compile_rule_dict(data)))
