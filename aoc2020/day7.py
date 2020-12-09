import sys
import unittest
import re
from collections import Counter
from toposort import toposort, toposort_flatten

class Day7Tests(unittest.TestCase):
    def test_parse(self):
        parsed = parse('light red bags contain 1 bright white bag, 2 muted yellow bags.')
        self.assertEqual([['light red', 'bright white'], ['light red', 'muted yellow']], parsed)
    
    def test_parsecontainsnone(self):
        parsed = parse('faded blue bags contain no other bags.')
        self.assertEqual([['faded blue', None]], parsed)

    def test_parsewithcounts(self):
        parsed = parse('light red bags contain 1 bright white bag, 2 muted yellow bags.')
        self.assertEqual([['light red', 'bright white'], ['light red', 'muted yellow']], parsed)
    
    def test_rulestonodes(self):
        rules =  parsefile('../_data/day7.txt')
        print(f'rule count:{len(rules)}')
        nodes = nodesfrom(rules)
        topo = list(toposort(nodes))

    def test_graphwalk(self):
        rules =  parsefile('../_data/day7_sample.txt')
        nodes = nodesfrom(rules, True)
        containers = walkup('light red', nodes)
        self.assertFalse(containers)
        containers = walkup('bright white', nodes)
        self.assertEqual({'light red', 'dark orange'}, containers)
        containers = walkup('shiny gold', nodes)
        self.assertEqual({'light red', 'bright white', 'muted yellow', 'dark orange'}, containers)   

    # def test_countbags(self):
    #     rules =  parsefile('../_data/day7_sample.txt')
    #     nodes = nodesfrom(rules, True)

        
def walkup(colour, nodes):
    containers = [k for k,v in nodes.items() if colour in v]
    if not containers:
        return set()
    
    results = set()
    for n in containers:
        results = results | {n} | walkup(n, nodes) 
    return results

def nodesfrom(rules, verbose=False):
    nodes = dict()
    for r in rules:
        if r[0] not in nodes:
            nodes[r[0]] = {r[-1]}
        else:
            nodes[r[0]].add(r[-1])
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
        c = [[subject.strip(), None]]
        if verbose:
            print(f'{line} -> {c}')
        return [[subject.strip(), None]]

    matches = re.findall('\d{1,}\s(?P<colour>.*?)\sbag(?:s?)', contents)
    colours = [[subject.strip(), c.strip()] for c in matches]
    if verbose:
        print(f'{line} -> {colours}')
    return colours

def main():
    rules =  parsefile('../_data/day7.txt')
    containers = walkup('shiny gold',nodesfrom(rules))
    #paths = sorted(paths, key=len)
    print(f'bags that can contain shiny gold: {len(containers)}')

if __name__ == '__main__':
    sys.exit(main())