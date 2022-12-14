from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,4)
test="""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
test1=2
test2=None

def parse(data):
    passports = [{x.split(":")[0]:x.split(":")[1] for x in passport.replace('\n',' ').split(" ")} for passport in "\n".join(data).split("\n\n")]      
    return passports

def is_valid_lax(passport):
    for field in ['byr','iyr','eyr','hgt','hcl','ecl','pid']:
        if field not in passport:
            # print(field)
            return False
    return True

def is_valid_strict(passport):
    rules = [
    len(passport['byr']) == 4,
    1920 <= int(passport['byr']) <= 2002,
    len(passport['iyr']) == 4,
    2010 <= int(passport['iyr']) <= 2020,
    len(passport['eyr']) == 4,
    2020 <= int(passport['eyr']) <= 2030,
    passport['hgt'][-2:] in ('in' , 'cm'),
    not (passport['hgt'][-2:]=='in') or (59 <= int(passport['hgt'][:-2])<=76) ,
    not (passport['hgt'][-2:]=='cm') or (150 <= int(passport['hgt'][:-2])<=193) ,
    passport['hcl'][0]=="#" and all([digit in '0123456789abcdef' for digit in passport['hcl'][1:]]),
    passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    len(passport['pid'])==9 and passport['pid'].isdigit()
    ]
    return all(rules)


@solution_timer(2020,4,1)
def part_one(data, verbose=False):
    passports = parse(data)
    return sum([is_valid_lax(passport) for passport in passports])


@solution_timer(2020,4,2)
def part_two(data, verbose=False):
    passports = parse(data)
    return sum([is_valid_lax(passport) and is_valid_strict(passport) for passport in passports])

if __name__ == "__main__":
    data = read_entire_input(2020,4)
    part_one(data)
    part_two(data)