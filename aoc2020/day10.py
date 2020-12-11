import sys
import unittest
from collections import Counter

class Tests(unittest.TestCase):
    def test_smallset(self):
        file = '../_data/day10_smallset.txt'
        adapters = parse(file)
        self.assertEqual(11, len(adapters))
        diffs = adapterdiffs(adapters)
        self.assertEqual({1:7, 3:5}, diffs)
    
    def test_mediumset(self):
        file = '../_data/day10_mediumset.txt'
        diffs = adapterdiffs(parse(file))
        self.assertEqual({1:22, 3:10}, diffs)

def adapterdiffs(adapters):
    adapters = sorted(adapters)
    builtin = adapters[-1] + 3
    adapters.append(builtin) # device
    adapters.insert(0, 0) # outlet

    s1 = adapters[0:-1]
    s2 = adapters[1:]
    diff = [a2 - a1 for (a1,a2) in zip(s1, s2)]

    return Counter(diff)

def parse(file):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        adapters = [int(line.strip()) for line in f]
    return adapters

def main():
    print('----------- Day 10 ----------')
    diffs = adapterdiffs(parse('../_data/day10.txt'))
    print(f'Diffs: {diffs}')
    print(f'1-jolt * 3-jolt = {diffs[1]} * {diffs[3]} = {diffs[1] * diffs[3]}')

if __name__ == '__main__':
    sys.exit(main())
