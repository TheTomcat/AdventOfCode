from typing import List, Dict, Tuple
from tqdm import tqdm
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

# This problem was an absolute headache. My solution is awful
# and I just don't have the strength to optimise it any further!

data = read_entire_input(2020,19)

def parse(data: List[str]) -> Tuple[Dict[int, str], List[str]]:
    rules = {}
    messages = []
    to_message = False
    for row in data:
        if row == "":
            to_message = True
            continue
        if to_message:
            messages.append(row)
        else:
            num, rule = row.split(": ")
            if '"' in rule:
                rule = rule.strip('"')
            else:
                rule = [[int(j) for j in i.split(" ")] for i in rule.split(" | ")]
            rules[int(num)] = rule
    return rules, messages

def CNF(rules):
    term = []
    rmax = 0
    for symbol in rules:
        for rule in rules[symbol]:
            term.append((symbol, rule))
            if symbol >= rmax:
                rmax = symbol + 1
    # print(rmax)
    # print(term)
    cnf = []
    for symbol, rule in term:
        if len(rule) <= 2:
            cnf.append((symbol, rule))
        else:
            for i in range(0,len(rule)-1):
                if i==0:
                    cnf.append((symbol, [rule[i], rmax+i]))
                elif i == len(rule)-2:
                    cnf.append((rmax+i-1, rule[-2:]))
                else:
                    cnf.append((rmax+i-1, [rule[i],rmax+i+1]))
            rmax += len(rule)-1
    # return cnf
    unit = []
    # skip = []
    for symbol, rule in cnf:
        # if symbol in skip:
        #     continue
        if len(rule) == 1 and isinstance(rule, list):
            for out_rule in rules[rule[0]]:
                unit.append((symbol, out_rule))
            # skip.append(rule[0])
        else:
            unit.append((symbol, rule))
    return unit

def expand(rule, rules):
    base = [[rules[i] if isinstance(i, int) else i for i in r] for r in rule] 
    # print("Base: ", base)
    new_rules = []
    for rule in base:
        acc = [[]] # A list of lists
        # print(f"Examining rule {rule}")
        for stage in rule:
            if isinstance(stage,str):
                # print(f"{stage} is a string")
                for i in acc:
                    i+=stage
                continue
            if len(stage)==1:
                # print(f"{stage} is a simple rule")
                for i in acc:
                    i+=stage[0]
                continue
            if len(stage) == 2:
                # print(f"{stage} is a complex rule")
                acc1 = [i.copy() for i in acc] 
                acc2 = [i.copy() for i in acc]
                # print("acc1: ",acc1)
                for i,j in zip(acc1, acc2):
                    i+=stage[0]
                    j+=stage[1]
                # print("acc1: ", acc1)
                acc = acc1+acc2
        new_rules+=acc
    # print(">>> returning")
    return new_rules

def run_all(base, rules):
    options = expand(base, rules)
    while True:
        new_opt = expand(options, rules)
        if new_opt != options:
            options = new_opt
            continue
        return new_opt

def consolidate(new_rules):
    options = []
    for rule in new_rules:
        options.append(''.join(rule))
    return options

def count_matching(messages, consolidated_rules):
    count = 0
    for message in messages:
        if message in consolidated_rules:
            count += 1
    return count

def evaluate(message, cnf):
    T = [[set([]) for j in message] for i in message]
    P = [[[0 for rule in cnf] for letter in message] for letter in message]
    for start, letter in enumerate(message):
        for symbol, rule in cnf:
            if isinstance(rule, str) and rule == letter:
                T[0][start].add(symbol)
                #P[0][start][symbol]=1
    for ssl in range(2,len(message)+1):
        for start in range(len(message)-ssl+1):
            for split in range(1,ssl):
                for symbol, rule in cnf:
                    if isinstance(rule, str):
                        continue
                    # if P[split-1][start][rule[0]] and P[ssl-split-1][start+split][rule[1]]:
                    #     P[ssl-1][start][symbol]=1
                    if rule[0] in T[split-1][start] and rule[1] in T[ssl-split-1][start+split]:
                        T[ssl-1][start].add(symbol)
                    # if rule[0] in T[split][start] and rule[1] in T[ssl-split][start+split]:
                        # T[ssl][start].add(symbol)
    # pprint(P)
    # return P[-1][0][0]
    # pprint(T)
    return 0 in T[-1][0]

@solution_timer(2020,19,1)
def part_one(data, verbose=False):
    rules, messages = parse(data)
    cnf = CNF(rules)
    
    count=0
    for message in messages:
        if evaluate(message,cnf):
            count += 1
    return count

def replace(rules):
    rules[8].append([42,8])
    rules[11].append([42,11,31])
    return rules

@solution_timer(2020,19,2)
def part_two(data, verbose=False):
    rules, messages = parse(data)
    rules = replace(rules)
    cnf = CNF(rules)
    
    count=0
    for message in messages:
        if evaluate(message,cnf):
            count += 1
    return count

if __name__ == "__main__":
    data = read_entire_input(2020,19)
    part_one(data)
    part_two(data)