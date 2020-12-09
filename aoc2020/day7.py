import sys
import unittest
import re
from collections import Counter
from toposort import toposort, toposort_flatten

class Day7Tests(unittest.TestCase):
    def test_parse(self):
        parsed = parse('light red bags contain 1 bright white bag, 2 muted yellow bags.')
        self.assertEqual([('light red', 'bright white', 1), ('light red', 'muted yellow', 2)], parsed)
    
    def test_parsecontainsnone(self):
        parsed = parse('faded blue bags contain no other bags.')
        self.assertEqual([('faded blue', None, 0)], parsed)

    def test_parsewithcounts(self):
        parsed = parse('light red bags contain 1 bright white bag, 2 muted yellow bags.')
        self.assertEqual([('light red', 'bright white', 1), ('light red', 'muted yellow',2)], parsed)
    
    def test_rulestonodes(self):
        rules =  parsefile('../_data/day7.txt')
        print(f'rule count:{len(rules)}')
        nodes = nodesfrom(rules)
        topo = list(toposort(nodes))

    def test_graphwalk(self):
        rules =  parsefile('../_data/day7_sample.txt')
        nodes = nodesfrom(rules)
        containers = walkup('light red', nodes)
        self.assertFalse(containers)
        containers = walkup('bright white', nodes)
        self.assertEqual({'light red', 'dark orange'}, containers)
        containers = walkup('shiny gold', nodes)
        self.assertEqual({'light red', 'bright white', 'muted yellow', 'dark orange'}, containers)

    def test_countbags(self):
        rules =  parsefile('../_data/day7_sample.txt')
        nodes = nodesfrom(rules)
        self.assertEqual(0, countbags('faded blue', nodes))
        self.assertEqual(5 + 6, countbags('vibrant plum', nodes, True))
        self.assertEqual(32, countbags('shiny gold', nodes, True))

    def test_findtuple(self):
        l = {('a', 1), ('b', 2)}
        self.assertTrue('a' in [c for c,_ in l])

def countbags(colour, nodes, verbose=False):
    if nodes[colour] == {(None, 0)}:
        return 0
    
    bags = 0
    contained = [n for n in nodes[colour]]
    for bag, count in contained:
        if verbose:
            print(f'bag: {bag}, count: {count}')
        bags += count + count * countbags(bag, nodes)
    return bags

def walkup(colour, nodes):
    containers = [k for k,val in nodes.items() if colour in [c for c,_ in val]]
    if not containers:
        return set()
    
    results = set()
    for n in containers:
        results = results | {n} | walkup(n, nodes) 
    return results

def nodesfrom(rules, verbose=False):
    nodes = dict()
    for l,r,num in rules:
        if l not in nodes:
            nodes[l] = {(r, num)}
        else:
            nodes[l].add((r, num))
    if verbose:
        for n,v in nodes.items():
            print(f'{n}: {v}')
    return nodes

def parsefile(file, verbose = False):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        rules = [r for line in f for r in parse(line, verbose)]
    return rules        

def parse(line, verbose = False):
    subject, contents = line.split('bags contain')
    if 'no other bags' in contents:
        c = [(subject.strip(), None, 0)]
        if verbose:
            print(f'{line} -> {c}')
        return c

    r = re.compile('(?P<bagcount>\d{1,})\s(?P<colour>.*?)\sbag(?:s?)')
    colours = [(subject.strip(), m['colour'].strip(), int(m['bagcount'])) for m in r.finditer(contents)]
    if verbose:
        print(f'{line} -> {colours}')
    return colours

def main():
    rules =  parsefile('../_data/day7.txt')
    nodes = nodesfrom(rules)
    containers = walkup('shiny gold',nodes)
    print(f'bags that can contain shiny gold: {len(containers)}')

    count = countbags('shiny gold', nodes)
    print(f'bags that shiny gold contains: {count}')

if __name__ == '__main__':
    sys.exit(main())