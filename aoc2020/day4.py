import sys
import unittest
import re

class Day4Tests(unittest.TestCase):
    def test_loadfile(self):
        passports = parse_passports('../_data/day4_sample.txt')
        self.assertEqual(len(passports), 4)
    
    def test_passportdata(self):
        passports = parse_passports('../_data/day4_sample.txt')
        expected = {'ecl':'gry', 'pid':'860033327', 'eyr':'2020', 'hcl':'#fffffd', 'byr':'1937', 'iyr':'2017', 'cid':'147', 'hgt':'183cm'}
        self.assertEqual(expected, passports[0])
        self.assertTrue('hgt' not in passports[1])
        self.assertTrue('cid' not in passports[2])
        self.assertTrue(all(k not in passports[3] for k in ('cid','byr')))

    def test_validate(self):
        passports = parse_passports('../_data/day4_sample.txt')
        self.assertTrue(valid(passports[0]))
        self.assertFalse(valid(passports[1]))
        self.assertTrue(valid(passports[2]))
        self.assertFalse(valid(passports[3]))
    
    def test_strict_invalidpassports(self):
        passports = parse_passports('../_data/day4pt2_invalid.txt')
        for p in passports:
            self.assertFalse(valid(p, True))

    def test_strict_validpassports(self):
        passports = parse_passports('../_data/day4pt2_valid.txt')
        for p in passports:
            self.assertTrue(valid(p, True))

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


def valid_ecl(ecl, verbose=False):
    is_valid = ecl in {'amb','blu','brn','gry','grn','hzl','oth'}
    if verbose:
        print(f'ecl:{ecl} {is_valid}')

def valid_hcl(hcl, verbose=False):
    is_valid = re.match('#[0-9a-f]{6}', hcl) is not None
    if verbose:
        print(f'hcl:{hcl} {is_valid}')
    return is_valid
        
def valid_hgt(hgt, verbose=False):
    is_valid = False
    if 'in' in hgt:
        num = int(hgt.strip('in'))
        is_valid = num >= 59 and num <= 76
    if 'cm' in hgt:
        num = int(hgt.strip('cm'))
        is_valid = num >= 150 and num <= 193
    if verbose:
        print(f'hgt {hgt}: {is_valid}')
    return is_valid

def in_range(date, min, max, verbose=False):
    year = int(date)
    is_valid = year >= min and year <= max
    if verbose:
        print(f'{date}: {is_valid}')
    return is_valid

def valid_eyr(eyr, verbose=False):    
    return in_range(eyr, 2020, 2030, verbose)

def valid_iyr(iyr, verbose=False):    
    return in_range(iyr, 2010, 2020, verbose)

def valid_byr(byr, verbose=False):
    return in_range(byr, 1920, 2002, verbose)

def diff_fields(required, passport):
    given = set(passport.keys())
    diff = given.difference(required).union(required.difference(given))
    return diff

def valid(passport, verbose=False):
    required = {'ecl','pid','eyr','hcl','byr','iyr','hgt'}
    has_required = all(k in passport for k in required)
    diff = diff_fields(required, passport)
    if verbose:
        print(f'{has_required}, fields diff: {diff}')
    if not(has_required):
        return False
    
    byr,eyr,iyr = valid_byr(passport['byr'],False), valid_eyr(passport['eyr'], False), valid_iyr(passport['iyr'], False)
    hgt, hcl, ecl = valid_hgt(passport['hgt'], False), valid_hcl(passport['hcl'], verbose), valid_ecl(passport['ecl'], verbose)
    
    return has_required and byr and eyr and iyr and hgt and hcl

def parse_passports(filename):
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
    print(len([p for p in parse_passports('../_data/day4.txt') if valid(p, verbose=True)]))

if __name__ == '__main__':
    unittest.main()
    #sys.exit(main())