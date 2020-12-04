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
        self.assertTrue(all (k not in passports[3] for k in ('cid','byr')))

    def test_validate(self):
        passports = parse_passports('../_data/day4_sample.txt')
        self.assertTrue(valid(passports[0]))

def valid(passport):
    return all (k in passport for k in ('ecl','pid','eyr','hcl','byr','iyr','hgt'))

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
    print('main')

if __name__ == '__main__':
    unittest.main()
    #sys.exit(main())