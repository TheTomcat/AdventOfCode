from collections import defaultdict

def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    # departure time: 45-533 or 547-970
    lines = text.split('\n')
    ionl = lines.index("")
    rule_dict = {}
    for line in lines[:ionl]:
        command, ruletext = line.split(": ")
        rules_raw = ruletext.split(" or ")
        rule_dict[command] = []
        for rule in rules_raw:
            l,u = (int(i) for i in rule.split("-"))
            rule_dict[command].append((l,u))
    # return rule_dict
    my_ticket = [int(i) for i in lines[lines.index("your ticket:") + 1].split(",")]
    others_start_at = lines.index("nearby tickets:") + 1
    other_tickets = []
    for ticket in lines[others_start_at:]:
        other_tickets.append([int(i) for i in ticket.split(',')])
    return rule_dict, my_ticket, other_tickets


def check_rule(rule, val):
    for l,u in rule:
        if (l <= val <= u):
            return True
    return False

def valid(ticket, rule_dict):
    return all([any([check_rule(rule_dict[rule],field) for rule in rule_dict]) for field in ticket])
    
def find_error(ticket, rule_dict):
    count = 0
    for field in ticket:
        if not any([check_rule(rule_dict[rule],field) for rule in rule_dict]):
            count += field
    return count

def make_ticket(rule_dict):
    return {key:None for key in rule_dict}

rule_dict, my_ticket, other_tickets = process(read_input(16))

def calculate_error_rate(other_tickets, rule_dict):
    count=0
    for ticket in other_tickets:
        if not valid(ticket, rule_dict):
            count += find_error(ticket, rule_dict)
    return count

print(calculate_error_rate(other_tickets, rule_dict))

def assign_fields(other_tickets, rule_dict):
    fields = [[] for _ in rule_dict] # Each potential field is a list of values
    for ticket in other_tickets:
        if not valid(ticket, rule_dict):
            continue
        for fi, field_val in enumerate(ticket):
            fields[fi].append(field_val)
    # print(fields[0][:10])
    potential_mapping = {rule:[] for rule in rule_dict}
    for fi, field in enumerate(fields):
        # Try and fit to a rule
        for rule in rule_dict:
            if all([check_rule(rule_dict[rule], val) for val in field]):
                potential_mapping[rule].append(fi)
    rule_heirachy = [rule for rule in potential_mapping]
    rule_heirachy.sort(key=lambda x: len(potential_mapping[x]))
    mapping = {}
    for rule in rule_heirachy:
        # If there is only one possibility left
        if len(potential_mapping[rule]) == 1:
            fi = potential_mapping[rule][0]
            mapping[rule] = fi
            for rule in potential_mapping:
                if fi in potential_mapping[rule]:
                    potential_mapping[rule].remove(fi)
        else:
            print("No i need more logic")
            break
    return mapping

print(assign_fields(other_tickets, rule_dict))

mapping = assign_fields(other_tickets, rule_dict)
val = 1
for rule in rule_dict:
    if rule.startswith('departure'):
        val *= my_ticket[mapping[rule]]
print(val)
