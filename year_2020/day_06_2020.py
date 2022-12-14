from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,6)
test="""abc

a
b
c

ab
ac

a
a
a
a

b""".split('\n')
test1=11
test2=6

def parse(data):
    groups = [[]]
    i=0
    for row in data:
        if row == "":
            i+=1
            groups.append([])
        else:
            groups[i].append(row)
    return groups

def custom_form_any(responses):
    form = {i: False for i in 'qwertyuiopasdfghjklzxcvbnm'}
    for response in responses:
        for question in form:
            if question in response:
                form[question] = True
    return form

def custom_form_all(responses):
    form = {i: True for i in 'qwertyuiopasdfghjklzxcvbnm'}
    for response in responses:
        for question in form:
            if question not in response:
                form[question] = False
    return form

@solution_timer(2020,6,1)
def part_one(data, verbose=False):
    groups = parse(data)
    count = 0
    for group in groups:
        count += len([val for val in custom_form_any(group).values() if val])
    return count

@solution_timer(2020,6,2)
def part_two(data, verbose=False):
    groups = parse(data)
    count = 0
    for group in groups:
        count += len([val for val in custom_form_all(group).values() if val])
    return count

if __name__ == "__main__":
    data = read_entire_input(2020,6)
    part_one(data)
    part_two(data)