import sys
import unittest
from collections import Counter

class Day6Tests(unittest.TestCase):
    def test_counter(self):
        group = Counter('abc')
        self.assertEquals(group['a'], 1)
    
    def test_sample(self):
        with open('../_data/day6_sample.txt', 'r', newline='', encoding='utf-8') as f:
            groups = [Counter()]
            g = 0
            for line in f:                
                answers = line.rstrip()
                print(answers)
                if answers == '':
                    g += 1
                    groups.append(Counter())
                    print(len(groups))
                else:
                    groups[g] += Counter(answers)
        print(groups)
        self.assertEquals(sum([len(g) for g in groups]), 11)                            

def main():    
    print('Day 6')

if __name__ == '__main__':
    sys.exit(main())