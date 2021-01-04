def read_input():
    with open('2020/2/input.txt', 'r') as f:
        for line in f:
            yield line

def process_line(line):
    hyph = line.find('-')
    sp = line.find(' ')
    col = line.find(':')
    sp2 = line.find(' ',col)
    lower = int(line[:hyph])
    upper = int(line[hyph+1:sp])
    c = line[sp+1:col]
    pw = line[col+2:]
    return (lower, upper, c, pw)

def validate_password1():
    c=0
    for line in read_input():
        lower, upper, count, password = process_line(line)
        if lower <= password.count(count) <= upper:
            c=c+1
    return c

def validate_password2():
    c=0
    for line in read_input():
        lower, upper, count, password = process_line(line)
        if (password[lower-1] == count) != (password[upper-1] == count):
            c=c+1
    return c

print(validate_password2())