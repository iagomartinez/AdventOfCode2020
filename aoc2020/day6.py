import sys
import unittest
from math import trunc
from collections import Counter

class Day6Tests(unittest.TestCase):
    def test_counter(self):
        group = Counter('abc')
        self.assertEqual(group['a'], 1)
    
    def test_count_groupanswers(self):
        groups = groupanswers('../_data/day6_sample.txt')
        self.assertEqual(sum([len(g) for g in groups]), 11) 
    
    def test_filteroutpartialanswers(self):
        answers = Counter('aab')
        answers = filteroutpartialanswers(answers, 2)
        self.assertEqual(Counter({'a':1, 'b':0}), answers)

    def test_count_wholegroupanswers(self):
        total = countwholegroupanswers('../_data/day6_sample.txt', True)
        self.assertEqual(total, 6) 

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

def filteroutpartialanswers(answercounter, memcount):
    newcounter = Counter()
    for a in answercounter.elements():
        newcounter[a] = trunc(answercounter[a] / memcount)
    return newcounter

def wholegroupanswers(file, verbose=False):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        g = 0
        memcount = 0
        groups = [(Counter(), 0)]
        for line in f:                
            answers = line.rstrip()
            if answers == '':
                g += 1
                memcount = 0
                groups.append((Counter(), 0))
            else:
                memcount += 1
                group, _ = groups[g]
                group += Counter(answers)
                groups[g] = group, memcount
    return groups

def countwholegroupanswers(file, verbose=False):
    groups = [filteroutpartialanswers(group, memcount) for group, memcount in wholegroupanswers(file, verbose)]

    if verbose:
        print(groups[0])
        print(groups[-1])
    
    agg = sum(groups, Counter())

    return sum(agg.values(), 0)

def main():    
    print('####### Day 6 #########')
    groups = groupanswers('../_data/day6.txt', True)
    allansweredquestions = sum([len(g) for g in groups])
    print(f'all answered questions: {allansweredquestions}')
    wholegroupanswers = countwholegroupanswers('../_data/day6.txt', True)
    print(f'whole group answers: {wholegroupanswers}')

if __name__ == '__main__':
    sys.exit(main())