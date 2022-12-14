from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,2)
test="""1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
test1=2
test2=1
def parse(data):
    validations = []
    for row in data:
        hyph = row.find('-')
        sp = row.find(' ')
        col = row.find(':')
        sp2 = row.find(' ',col)
        lower = int(row[:hyph])
        upper = int(row[hyph+1:sp])
        c = row[sp+1:col]
        pw = row[col+2:]
        validations.append((lower, upper, c, pw))
    return validations

@solution_timer(2020,2,1)
def part_one(data, verbose=False):
    validations = parse(data)
    c=0
    for lower, upper, count, password in validations:
        if lower <= password.count(count) <= upper:
            c=c+1
    return c

@solution_timer(2020,2,2)
def part_two(data, verbose=False):
    validations = parse(data)
    c=0
    for lower, upper, count, password in validations:
        if (password[lower-1] == count) != (password[upper-1] == count):
            c=c+1
    return c

if __name__ == "__main__":
    data = read_entire_input(2020,2)
    part_one(data)
    part_two(data)