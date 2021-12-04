def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(string):
    data = [0] + [int(i) for i in string.split('\n')]
    data = data + [max(data)+3]
    data.sort()
    return data

def make_chain(data):
    diff=[]
    for i in range(len(data)-1):
        diff.append(data[i+1]-data[i])
    return diff

test="""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

# tl = make_chain(process(test))
# print(tl.count(1), tl.count(3))

data = process(read_input(10))
chain = make_chain(data)
print(chain.count(1) * chain.count(3))

# Attempt 1 - too slow
def build_trees(data):
    forward = {}
    for node in data:
        forward[node] = []
        for i in range(node+1, node+4):
            if i in data:
                forward[node].append(i)
    backward = {}
    for node in reversed(data):
        backward[node] = []
        for i in range(node-3,node):
            if i in data:
                backward[node].append(i)
    return forward, backward

def count(tree, node, goal):
    if node == goal:
        return 1
    else:
        return sum([count(tree, i, goal) for i in tree[node]])

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

def count(data):
    counter=0
    expected_value = 0
    runs = []
    for node in data:
        if node == expected_value:
            counter += 1
            expected_value += 1
        else:
            runs.append(counter)
            counter = 1
            expected_value = node+1
    return runs

trib = {1:1, 2:2, 3:4, 4:7, 5:13, 6:24, 7:24+13+7}

# data = process(test)
# print(data)
gaps = count(data)
# print(gaps)
numpaths = [trib[i-1] for i in gaps if i >= 2]

i=1
for val in numpaths:
    i*=val
print(i)