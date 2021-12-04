def read_input():
    with open('2020/1/input.txt', 'r') as f:
        for line in f:
            yield line

def process_input():
    return [int(i) for i in read_input()]

def solution1():
    inputs = process_input()
    for i, first_number in enumerate(inputs):
        for second_number in inputs[i+1:]:
            third_number = 2020 - first_number - second_number
            if third_number in inputs:
                print(first_number, second_number, third_number, first_number*second_number*third_number)

solution1()