from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,1)
test = """1721
979
366
299
675
1456"""
test1=514579
test2=241861950

def parse(data):
    return [int(i) for i in data]

@solution_timer(2020,1,1)
def part_one(data, verbose=False):
    expense_report = parse(data)
    for i, first_number in enumerate(expense_report):
        second_number = 2020 - first_number
        if second_number in expense_report:
                return first_number * second_number

@solution_timer(2020,1,2)
def part_two(data, verbose=False):
    expense_report = parse(data)
    for i, first_number in enumerate(expense_report):
        for second_number in expense_report[i+1:]:
            third_number = 2020 - first_number - second_number
            if third_number in expense_report:
                return first_number * second_number * third_number

if __name__ == "__main__":
    data = read_entire_input(2020,1)
    part_one(data)
    part_two(data)