import sys
import unittest

class Day9Tests(unittest.TestCase):
    def test_preambleset(self):
        numbers = parse('../_data/day9_sample.txt')
        validset = calculateset(0, 5, numbers)
        self.assertTrue(20, len(validset))

    def test_findinvalidnumber(self):
        numbers = parse('../_data/day9_sample.txt')
        invalid, _ = findinvalid(0, 5, numbers)
        self.assertEqual(127,invalid)

    def test_findweakness(self):
        numbers = parse('../_data/day9_sample.txt')
        weakness = findweakness(0, 5, numbers) 
        self.assertEqual(62, weakness)

def findweakness(start, preamble, numbers, verbose=False):
    invalid, pos = findinvalid(start, preamble, numbers)
    searchset = numbers[0:pos+1]
    weakness=None
    for length in range(2, pos+1):
        for i in range(0, pos-length):
            window = searchset[i:i+length]
            if verbose:
                print(f'window: {window}')
            if sum(window) == invalid:
                if verbose:
                    print(f'found weakness: {max(window)} {min(window)}')
                weakness = max(window) + min(window)
                return weakness

def findinvalid(start, preamble, numbers):
    for ix, num in enumerate(numbers[preamble:]):
        valid = calculateset(start, preamble, numbers)
        if num not in valid:
            return num, ix
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
    weakness = findweakness(0, 25, numbers, True)
    print(f'XMAS weakness: {weakness}')

if __name__ == '__main__':
    sys.exit(main())
