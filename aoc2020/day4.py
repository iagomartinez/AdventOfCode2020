import sys
import unittest

class Day4Tests(unittest.TestCase):
    def test_loadfile(self):
        with open('../_data/day4_sample.txt', 'r', newline='', encoding='utf-8') as f:
            passports = parse_file(f)
            self.assertEqual(len(passports), 4)

def parse_file(file):
    return []

def main():
    print('main')

if __name__ == '__main__':
    unittest.main()
    #sys.exit(main())