from typing import List, Tuple

from lib.iterators import grouper


def split(seedlist: List['int'], split_at: int) -> List['int']:
    """Takes a seed list [start1, length1, start2, length2, ...] 
    and splits it at split_at, returning a new seed list"""
    output = []
    for start, length in  grouper(2, seedlist):
        if start <= split_at < start + length:
            l1 = split_at - start
            l2 = length - l1
            output.extend([start, l1, split_at, l2])
        else:
            output.extend([start, length])
    return output

def intersects(seed: Tuple[int,int]):
    def f(mapping: Tuple[int,int,int]):
        nonlocal seed
        start, length = seed
        end = start + length
        rstart, dstart, mlength = mapping
        dend = dstart + mlength
        return (dstart <= start < dend or  # Seed start in map
                dstart <= end < dend or    # Seed end in map
                start < dstart < dend < end) # Seed fully contains map
    return f

def find_splits(seed: Tuple[int,int], mapping: List[Tuple[int,int,int]]):
    start, length = seed
    end = start + length
    filtered_maps = list(filter(intersects(seed), mapping))
    print(filtered_maps)

def intersections(seedlist: List[int], mapping: List[Tuple[int,int,int]]):
    index = 0
    while index < len(seedlist):
        start = seedlist[index]
        length = seedlist[index+1]
        end = start + length

        for r_start, d_start, m_length in mapping:
            ...
            # d_end = d_start + m_length
            # # <---> |--|
            # if d_end < start:
            #     continue
            # # <----|-->---|
            # # <--->|<->---|
            # elif start <= d_end < end:
            #     l1 = 

