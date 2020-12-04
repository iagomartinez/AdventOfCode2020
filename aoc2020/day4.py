import sys
import unittest

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
    
    def test_strictinvalidpassports(self):
        passports = parse_passports('../_data/day4pt2_invalid.txt')
        for p in passports:
            self.assertFalse(valid(p))

    def test_byr(self):
        self.assertTrue(valid_byr('2002'))
        self.assertFalse(valid_byr('2003'))
        self.assertTrue(valid_byr('1920'))
        self.assertFalse(valid_byr('1919'))

def valid_byr(byr, verbose=False):
    try:
        year = int(byr)
    except ValueError:        
        print('invalid byr {byr}')
        return False
    is_valid = year >= 1920 and year <= 2002
    print(f'{byr}: {is_valid}')
    return is_valid

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
    return has_required and valid_byr(passport['byr'],verbose)

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