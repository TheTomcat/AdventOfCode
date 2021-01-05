def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    raw_tiles = text.split('\n\n')
    tiles = {}
    for tile in raw_tiles:
        rows = tile.split('\n')
        index = rows[0][5:9]
        data = rows[1:]
        tiles[int(index)] = data
    return tiles



print(process(read_input(20)))