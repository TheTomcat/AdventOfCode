def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    return text.split('\n')

def tokenise(exp):
    exp = exp.replace(" ","")
    output = []
    numeric_token = ''
    for character in exp:
        if character in '+*()':
            if numeric_token:
                output.append(int(numeric_token))
            output.append(character)
            numeric_token = ''
        else:
            numeric_token += character
    if numeric_token:
        output.append(int(numeric_token))
    return output

def evaluate_bracketed_expression(exp):
    i=0
    while True:
        if ")" in exp:
            i_close = exp.index(")",i)
            for index in range(i_close,-1,-1):
                if exp[index] == "(":
                    i_open = index
                    break
            exp[i_open:i_close+1] = [evaluate_simple_expression(exp[i_open+1:i_close])]
            i=i_open
        else:
            return evaluate_simple_expression(exp)
    
def evaluate_simple_expression(exp):
    if len(exp)==1:
        return exp[0]
    if len(exp) == 0:
        return
    if '(' in exp:
        print(exp)
        raise ValueError("Cannot parse '(' in simple expression")

    n1 = int(exp[0])
    op = exp[1]
    n2 = int(exp[2])
    res = opl[op](n1,n2)
    exp = [res] + exp[3:]
    return evaluate_simple_expression(exp)

def add(a,b):
    return a+b
def mul(a,b):
    return a*b
opl = {"+":add,
       "*":mul}

# print(evaluate_bracketed_expression(tokenise("1+(2*3)")))

print(tokenise("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

print(evaluate_bracketed_expression(tokenise("2 * 3 + (4 * 5)")), 26)
print(evaluate_bracketed_expression(tokenise("5 + (8 * 3 + 9 + 3 * 4 * 3)")),437)
print(evaluate_bracketed_expression(tokenise("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")),12240)
print(evaluate_bracketed_expression(tokenise("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")),13632)

tots = []
for exp in process(read_input(18)):
    tok = tokenise(exp)
    tots.append(evaluate_bracketed_expression(tok))
print(sum(tots))