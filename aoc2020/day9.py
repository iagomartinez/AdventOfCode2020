import sys
import unittest

class Day9Tests(unittest.TestCase):
    def test_preambleset(self):
        numbers = parse('../_data/day9_sample.txt')
        validset = calculateset(0, 5, numbers)
        self.assertTrue(20, len(validset))

    def test_findinvalidnumber(self):
        numbers = parse('../_data/day9_sample.txt')
        invalid = findinvalid(0, 5, numbers)
        self.assertEqual(127,invalid)

def findinvalid(start, preamble, numbers):
    for num in numbers[preamble:]:
        valid = calculateset(start, preamble, numbers)
        if num not in valid:
            return num
        start +=1

def calculateset(start, length, numbers):
    preamble = numbers[start:start + length]
    return {n + m for n in preamble for m in preamble if n != m}

def parse(file):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        numbers = [int(n.strip()) for n in f]
    return numbers

def main():
    print('---------- Day 9 ----------')
    numbers = parse('../_data/day9.txt')
    invalid = findinvalid(0, 25, numbers)
    print(f'First invalid number: {invalid}')

if __name__ == '__main__':
    sys.exit(main())
