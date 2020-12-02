import sys
import unittest

class ValidationTests(unittest.TestCase):
    def test_parse(self):
        parsed = parse('2-8 t: pncmjxlvckfbtrjh')
        self.assertTupleEqual(parsed, (2,8,'t','pncmjxlvckfbtrjh'))

    def test_is_valid(self):
        self.assertTrue(is_valid('1-3 a: abcde'))
        self.assertFalse(is_valid('1-3 b: cdefg'))
        self.assertFalse(is_valid('2-9 c: ccccccccc'))

def parse(line):
    policy, password = line.split(': ')
    range, char = policy.split(' ')
    min,max = range.split('-')
    return (int(min),int(max),char,password)

def is_valid(line):
    min, max, char, password = parse(line)
    return None

def main():
    with open('../_data/day2.txt', 'r',newline='', encoding='utf-8') as f:
        print(len([1 for line in f if is_valid(line)]))

if __name__ == '__main__':
    unittest.main()
    sys.exit(main())
