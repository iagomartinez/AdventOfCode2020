import sys
import unittest
from functools import reduce
from collections import Counter

class Tests(unittest.TestCase):
    def test_smallset(self):
        file = '../_data/day10_smallset.txt'
        adapters = loadadapters(file)
        self.assertEqual(13, len(adapters))
        diffs = joltagediffs(adapters)
        self.assertEqual({1:7, 3:5}, diffs)
    
    def test_mediumset(self):
        file = '../_data/day10_mediumset.txt'
        diffs = joltagediffs(loadadapters(file))
        self.assertEqual({1:22, 3:10}, diffs)

    def test_findarrangements(self):
        file = '../_data/day10_mediumset.txt'
        adapters = loadadapters(file)
        permutations = countpermutations(adapters)
        self.assertEqual(19208, permutations)

def countpermutations(adapters):
    #   How this works:
    #   1. Where joltage diff is 3 between an adapter and the one before or after, that adapter is fixed
    #   2. Adapters that are not fixed can be removed, and will be in sets of 1, 2, or 3
    #   3. The total possibilities are the product of the possible combinations for each set of removeable adapters
    #   4. For sets of 3, there is a maximum of 7 combinations, as all 3 adapters cannot be removed (because the gap between remaining adapters would be > 3)
    removeables=[]
    for i in range(1,len(adapters)):
        if adapters[i] - adapters[i-1] < 3 and adapters[i+1] - adapters[i] < 3:
            removeables.append(adapters[i])
    sets = []
    collector = [removeables[0]]
    for a in removeables[1:]:
        if a == collector[-1] + 1:
            collector.append(a)
        else:
            sets.append(collector)
            collector=[a]
    sets.append(collector)
    spans = [len(s) for s in sets]
    possibilities = [2**s if s < 3 else (2**s - 1) for s in spans]
    permutations = reduce((lambda x, y: x*y), possibilities)
    return permutations

def joltagediffs(adapters):
    s1 = adapters[0:-1]
    s2 = adapters[1:]
    diff = [a2 - a1 for (a1,a2) in zip(s1, s2)]
    return Counter(diff)

def loadadapters(file):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        adapters = sorted([int(line.strip()) for line in f])
    adapters.append(adapters[-1] + 3) # device
    adapters.insert(0, 0) # outlet
    return adapters

def main():
    print('----------- Day 10 ----------')
    adapters = loadadapters('../_data/day10.txt')
    diffs = joltagediffs(adapters)
    print(f'Diffs: {diffs}')
    print(f'1-jolt * 3-jolt = {diffs[1]} * {diffs[3]} = {diffs[1] * diffs[3]}')
    permutations = countpermutations(adapters)
    print(f'Possible arrangements: {permutations}')

if __name__ == '__main__':
    sys.exit(main())
