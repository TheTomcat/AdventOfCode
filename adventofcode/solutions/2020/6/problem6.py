def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def consolidate_questions(list_of_strs):
    consol = {i:True for i in 'qwertyuiopasdfghjklzxcvbnm'}
    for response in list_of_strs:
        responses = list(response)
        for answer in 'qwertyuiopasdfghjklzxcvbnm':
            if answer not in responses:
                consol[answer]=False
    return consol

def count_for_each(data):
    groups = data.split('\n\n')
    total = 0
    for group in groups:
        response = group.split('\n')
        total += len([val for key,val in consolidate_questions(response).items() if val])
    return total

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

b"""

print(count_for_each(test))
print(count_for_each(read_input(6)))