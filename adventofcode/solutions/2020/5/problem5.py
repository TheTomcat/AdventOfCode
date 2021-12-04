def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process_seats(input_string):
    seats = input_string.split('\n')
    ids = []
    for seat in seats:
        row = seat[:7].replace('F','0').replace('B','1')
        row = int(row,base=2)
        col = seat[-3:].replace('R','1').replace('L','0')
        col = int(col, base=2)
        ids.append(row*8+col)
    return ids

def find_missing_seat(ids):
    expected_id = ids[0]
    for seat in ids:
        if seat != expected_id:
            return expected_id
        expected_id+=1

test="""FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""

process_seats(test)
print(max(process_seats(read_input(5))))

# Part 2

print(find_missing_seat(sorted(process_seats(read_input(5)))))