import sys
import unittest

class ValidationTests(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(True)
    
    def test_parse(self):
        parsed = parse('2-8 t: pncmjxlvckfbtrjh')
        self.assertTupleEqual(parsed, (2,8,'t','pncmjxlvckfbtrjh'))

def parse(line):
    policy, password = line.split(': ')
    range, char = policy.split(' ')
    min,max = range.split('-')
    return (int(min),int(max),char,password)

def main():
    with open('../_data/day2.txt', 'r',newline='', encoding='utf-8') as f:
        for line in f:
            print(line, end='')

if __name__ == '__main__':
    unittest.main()
    sys.exit(main())
