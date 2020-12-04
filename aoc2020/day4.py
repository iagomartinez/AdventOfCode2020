import sys
import unittest
import re

class Day4Tests(unittest.TestCase):
    def test_loadfile(self):
        passports = parse('../_data/day4_sample.txt')
        self.assertEqual(len(passports), 4)
    
    def test_passportdata(self):
        passports = parse('../_data/day4_sample.txt')
        expected = {'ecl':'gry', 'pid':'860033327', 'eyr':'2020', 'hcl':'#fffffd', 'byr':'1937', 'iyr':'2017', 'cid':'147', 'hgt':'183cm'}
        self.assertEqual(expected, passports[0])
        self.assertTrue('hgt' not in passports[1])
        self.assertTrue('cid' not in passports[2])
        self.assertTrue(all(k not in passports[3] for k in ('cid','byr')))

    def test_validate(self):
        passports = parse('../_data/day4_sample.txt')
        self.assertTrue(validpassport(passports[0]))
        self.assertFalse(validpassport(passports[1]))
        self.assertTrue(validpassport(passports[2]))
        self.assertFalse(validpassport(passports[3]))
    
    def test_strict_invalidpassports(self):
        passports = parse('../_data/day4pt2_invalid.txt')
        for p in passports:
            self.assertFalse(validpassport(p, True))

    def test_strict_validpassports(self):
        passports = parse('../_data/day4pt2_valid.txt')
        for p in passports:
            self.assertTrue(validpassport(p, True))

    def test_byr(self):
        self.assertTrue(valid_byr('2002'))
        self.assertFalse(valid_byr('2003'))
        self.assertTrue(valid_byr('1920'))
        self.assertFalse(valid_byr('1919'))

    def test_iyr(self):
        self.assertTrue(valid_iyr('2010'))
        self.assertTrue(valid_iyr('2020'))

        self.assertFalse(valid_iyr('2009'))
        self.assertFalse(valid_iyr('2021'))

    def test_eyr(self):
        self.assertTrue(valid_eyr('2020'))
        self.assertTrue(valid_eyr('2025'))
        self.assertTrue(valid_eyr('2030'))

        self.assertFalse(valid_eyr('2019'))
        self.assertFalse(valid_eyr('2031'))
    
    def test_hgt(self):
        self.assertTrue(valid_hgt('60in'))
        self.assertFalse(valid_hgt('190in'))
        self.assertFalse(valid_hgt('190'))

        self.assertTrue(valid_hgt('190cm'))
        self.assertTrue(valid_hgt('193cm'))
        self.assertFalse(valid_hgt('194cm'))
        self.assertFalse(valid_hgt('149cm'))

    def test_hcl(self):
        self.assertTrue(valid_hcl('#123abc'))
        self.assertFalse(valid_hcl('#123abz'))
        self.assertFalse(valid_hcl('123abc'))

    def test_ecl(self):        
        self.assertTrue(valid_ecl('amb'))
        self.assertFalse(valid_ecl(''))
        self.assertFalse(valid_ecl('xxx'))
    
    def test_pid(self):
        self.assertTrue(valid_pid('000000001'))
        self.assertFalse(valid_pid('0123456789'))

def valid_pid(pid):
    is_valid = pid.isnumeric() and len(pid) == 9
    return is_valid

def valid_ecl(ecl):
    is_valid = ecl in {'amb','blu','brn','gry','grn','hzl','oth'}
    return is_valid

def valid_hcl(hcl):
    is_valid = re.match('#[0-9a-f]{6}', hcl) is not None
    return is_valid
        
def valid_hgt(hgt):
    is_valid = False
    if 'in' in hgt:
        num = int(hgt.strip('in'))
        is_valid = num >= 59 and num <= 76
    if 'cm' in hgt:
        num = int(hgt.strip('cm'))
        is_valid = num >= 150 and num <= 193
    return is_valid

def in_range(date, min, max):
    year = int(date)
    is_valid = year >= min and year <= max
    return is_valid

def valid_eyr(eyr):    
    return in_range(eyr, 2020, 2030)

def valid_iyr(iyr):    
    return in_range(iyr, 2010, 2020)

def valid_byr(byr):
    return in_range(byr, 1920, 2002)

def diff_fields(required, passport):
    given = set(passport.keys())
    diff = given.difference(required).union(required.difference(given))
    return diff

def valid_fields(passport):
    required = {'ecl','pid','eyr','hcl','byr','iyr','hgt'}
    has_required = all(k in passport for k in required)
    diff = diff_fields(required, passport)
    return has_required, diff

def validpassport(passport, verbose=False):
    has_required, diff = valid_fields(passport)
    if not has_required:
        if verbose:
            print(f'Invalid fields! exceptions:{diff}')
        return False

    validate_map = {'byr': valid_byr, 'eyr': valid_eyr, 'iyr': valid_iyr, 'hgt': valid_hgt, 'hcl': valid_hcl, 'ecl': valid_ecl, 'pid':valid_pid}    
    tests = {f'{k}:{passport[k]}': fn(passport[k]) for k, fn in validate_map.items()}
    
    is_valid = has_required and all(tests.values())

    if verbose:
        print(f'Valid: {is_valid}, {tests}')

    return is_valid 

def parse(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        passports = []
        new_pass = dict()
        for line in f:
            clean_line = line.rstrip()
            if clean_line == '':
                passports.append(new_pass)
                new_pass = dict()
            else:
                fields = clean_line.split(' ')
                for f in fields:
                    k,v = f.split(':')
                    new_pass[k] = v
        
    passports.append(new_pass)    
    return passports

def main():
    print(len([p for p in parse('../_data/day4.txt') if validpassport(p, verbose=True)]))

if __name__ == '__main__':
    #unittest.main()
    sys.exit(main())