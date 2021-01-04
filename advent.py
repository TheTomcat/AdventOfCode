def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        for line in f:
            yield line
        