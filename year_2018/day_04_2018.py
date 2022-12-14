from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

import re
from collections import defaultdict, Counter

data = read_entire_input(2018,4)
test = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split("\n")

def parse(data: List[str]) -> Any:
    regex = r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)] (.+)'
    expression = re.compile(regex)
    records = []
    for record in data:
        year, month, day, hour, minute, description = expression.match(record).groups()
        if description == "falls asleep":
            description = "s"
        elif description == "wakes up":
            description = "w"
        else:
            description = int(''.join(i for i in description if i.isdigit()))
        records.append((int(year), int(month), int(day), int(hour),int(minute), description))
        
    return records

def process_records(records):
    records.sort()
    guard_id = None
    to_sleep = 0
    log = defaultdict(Counter)
    for _, _, _, _, min, desc in records:
        if isinstance(desc, int):
            guard_id = desc
        elif desc == 's':
            to_sleep = min
        elif desc == 'w':
            for i in range(to_sleep, min):
                log[guard_id][i] += 1
    return log

@solution_timer(2018,4,1)
def part_one(data: List[str], verbose=False):
    records = parse(data)
    log = process_records(records)
    
    sleepiest_guard_id = sorted([(i.total(), id) for id, i in log.items()], reverse=True)[0][1]
    sleepiest_minute = log[sleepiest_guard_id].most_common(1)[0][0]
    return sleepiest_guard_id*sleepiest_minute

@solution_timer(2018,4,2)
def part_two(data: List[str], verbose=False):
    records = parse(data)
    log = process_records(records)
    
    sleepiest_guard_id = sorted([(*i.most_common(1)[0][::-1], id) for id, i in log.items()], reverse=True)
    
    return sleepiest_guard_id[0][1] * sleepiest_guard_id[0][2]

if __name__ == "__main__":
    data = read_entire_input(2018,4)
    part_one(data)
    part_two(data)