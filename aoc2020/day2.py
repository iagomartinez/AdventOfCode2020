import sys
import unittest

class ValidationTests(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(True)
    
    def test_parse(self):
        parsed = parse('2-8 t: pncmjxlvckfbtrjh')
        self.assertTupleEqual(parsed, (2,8,'t','pncmjxlvckfbtrjh'))

    def test_is_valid_min_char(self):
        self.assertTrue(valid_min(2, 't', 'tt'))

    def test_is_not_valid_if_not_min_char(self):
        self.assertFalse(valid_min(2, 't', 'xxxxx'))
        self.assertFalse(valid_min(2, 't', 'xxxxxt'))
        self.assertFalse(valid_min(2, 't', ''))

    def test_is_valid_max(self):
        self.assertTrue(valid_max(8, 't', 'tt'))
        self.assertTrue(valid_max(8, 't', 't' * 8))
        self.assertTrue(valid_max(0, 't', 'xx'))
        self.assertTrue(valid_max(0, 't', ''))

    def test_is_not_valid_max(self):
        self.assertFalse(valid_max(8, 't', 't' * 9))


def parse(line):
    policy, password = line.split(': ')
    range, char = policy.split(' ')
    min,max = range.split('-')
    return (int(min),int(max),char,password)

def valid_min(min, char, password):
    return password.count(char) >= min

def valid_max(max, char, password):
    return password.count(char) <= max

def is_valid(min, max, char, password):
    return valid_min(min, char, password)

def main():
    with open('../_data/day2.txt', 'r',newline='', encoding='utf-8') as f:
        for line in f:
            print(line, end='')

if __name__ == '__main__':
    unittest.main()
    sys.exit(main())
