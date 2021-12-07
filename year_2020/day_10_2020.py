from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,10)

def parse(data):
    data = [0] + [int(i) for i in data]
    data = data + [max(data)+3]
    data.sort()
    return data

def make_chain(data):
    diff=[]
    for i in range(len(data)-1):
        diff.append(data[i+1]-data[i])
    return diff

@solution_timer(2020,10,1)
def part_one(data):
    adaptors = parse(data)
    chain = make_chain(adaptors)
    return chain.count(1) * chain.count(3)

# Attempt 2

# 5->6 = 1 -> 5,6
# 4->6 = 2 -> 4,(5->6) or 4,6
# 3->6 = 4 -> 3,(4->6) or 3,(5->6) or 3,6
# 2->6 = 7 -> 2,(3->6) or 2,(4->6) or 2,(5->6)
# 1->6 = 13-> 1,(2->6) or 1,(3->6) or 1,(4->6)
# 0->6 = 24-> 0,(1->6) or 0,(2->6) or 0,(3->6)

# Find runs of consecutive numbers
# find the lengths of each
# find the tribonacci numbers
# product them

def count(adaptors):
    counter=0
    expected_value = 0
    runs = []
    for node in adaptors:
        if node == expected_value:
            counter += 1
            expected_value += 1
        else:
            runs.append(counter)
            counter = 1
            expected_value = node+1
    return runs

@solution_timer(2020,10,2)
def part_two(data):
    adaptors = parse(data)
    trib = {1:1, 2:2, 3:4, 4:7, 5:13, 6:24, 7:24+13+7}

    gaps = count(adaptors)

    numpaths = [trib[i-1] for i in gaps if i >= 2]

    i=1
    for val in numpaths:
        i*=val
    return i


if __name__ == "__main__":
    data = read_entire_input(2020,10)
    part_one(data)
    part_two(data)