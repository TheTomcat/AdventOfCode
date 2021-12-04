from itertools import islice

def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result)==n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def find_fault(bits):
    for i in range(len(bits)-25):
        tot = bits[i+25]
        for num in bits[i:i+25]:
            if tot - num in bits[i:i+25]:
                break
        else:
            return tot

def break_cipher(bits):
    tot = find_fault(bits)
    for lower in range(len(bits)):
        for length in range(1, len(bits)-lower):
            add = sum(bits[lower:lower+length])
            if add > tot:
                break
            elif add == tot:
                return min(bits[lower:lower+length]) + max(bits[lower:lower+length])
            
stream = read_input(9)
bits = [int(i) for i in stream.split('\n')]
print(find_fault(bits))
print(break_cipher(bits))