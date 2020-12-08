import sys
import unittest
from collections import Counter

class Day6Tests(unittest.TestCase):
    def test_counter(self):
        group = Counter('abc')
        self.assertEqual(group['a'], 1)
    
    def test_sample(self):
        groups = groupanswers('../_data/day6_sample.txt')
        self.assertEqual(sum([len(g) for g in groups]), 11) 

    def test_countfullfilegroups(self):                           
        groups = groupanswers('../_data/day6.txt')
        self.assertEqual(len(groups), 504)

def groupanswers(file, verbose=False):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        groups = [Counter()]
        g = 0
        for line in f:                
            answers = line.rstrip()
            if answers == '':
                g += 1
                groups.append(Counter())
            else:
                groups[g] += Counter(answers)
    if verbose:
        print(groups[0])
        print(groups[-1])
    return groups

def main():    
    print('####### Day 6 #########')
    groups = groupanswers('../_data/day6.txt', True)
    print(sum([len(g) for g in groups]))

if __name__ == '__main__':
    sys.exit(main())