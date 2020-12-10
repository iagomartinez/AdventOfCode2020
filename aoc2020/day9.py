import sys
import unittest

class Day9Tests(unittest.TestCase):
    def test_preambleset(self):
        numbers = parse('../_data/day9_sample.txt')
        validset = calculateset(0, 5, numbers)
        self.assertTrue(20, len(validset))

    def test_findinvalidnumber(self):
        numbers = parse('../_data/day9_sample.txt')
        valid = calculateset(0, 5, numbers)
        invalid = set()
        start = 0
        for num in numbers[5:]:
            if num not in valid:
                invalid.add(num)
                break
            start +=1
            valid = calculateset(start, 5, numbers)
        self.assertEqual({127},invalid)

def calculateset(start, length, numbers):
    preamble = numbers[start:start + length]
    return {n + m for n in preamble for m in preamble if n != m}

def parse(file):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        numbers = [int(n.strip()) for n in f]
    return numbers

def main():
    print('Day 9')

if __name__ == '__main__':
    sys.exit(main())
