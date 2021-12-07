def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()


def is_valid(pdict):
    for field in ['byr','iyr','eyr','hgt','hcl','ecl','pid']:
        if field not in pdict:
            # print(field)
            return False
    rules = [
    len(pdict['byr']) == 4,
    1920 <= int(pdict['byr']) <= 2002,
    len(pdict['iyr']) == 4,
    2010 <= int(pdict['iyr']) <= 2020,
    len(pdict['eyr']) == 4,
    2020 <= int(pdict['eyr']) <= 2030,
    pdict['hgt'][-2:] in ('in' , 'cm'),
    not (pdict['hgt'][-2:]=='in') or (59 <= int(pdict['hgt'][:-2])<=76) ,
    not (pdict['hgt'][-2:]=='cm') or (150 <= int(pdict['hgt'][:-2])<=193) ,
    pdict['hcl'][0]=="#" and all([digit in '0123456789abcdef' for digit in pdict['hcl'][1:]]),
    pdict['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    len(pdict['pid'])==9 and pdict['pid'].isdigit()
    ]
    # print(rules)
    # print(pdict['hgt'][-2:], pdict['hgt'][:-2])
    return all(rules)
    # return True

def validate_batch(str_input):
    passports = str_input.split('\n\n')

    count = 0
    for passport in passports:
        slt = passport.replace('\n', ' ')
        kvps = slt.split(' ')
        pdict = {}
        # print(kvps)
        for kvp in kvps:
            key, value = kvp.split(':')
            pdict[key] = value
        if is_valid(pdict):
            count += 1
    return count

test = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

valids="""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

invalids="""eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""


# print(validate_batch(test))
print(validate_batch(read_input(4)))
print(validate_batch(valids))
print(validate_batch(invalids))

