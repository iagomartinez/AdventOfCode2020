import sys
import unittest
import re

class Day7Tests(unittest.TestCase):
    def test_parse(self):
        parsed = parse('light red bags contain 1 bright white bag, 2 muted yellow bags.')
        self.assertEqual([['light red', 'bright white'], ['light red', 'muted yellow']], parsed)
    
    def test_parsecontainsnone(self):
        parsed = parse('faded blue bags contain no other bags.')
        self.assertEqual([['faded blue', None]], parsed)

    def test_sample(self):
        rules = parsefile('../_data/day7_sample.txt')      
        self.assertEqual(len(rules), 15)
        paths = find('shiny gold', rules, [])
        paths = sorted(paths, key=len)#print(paths)
        for p in paths:
            print( p)
        self.assertEqual(len(paths), 4)        

    def test_simplecase(self):
        rules =  parsefile('../_data/day7_simplecase.txt')
        self.assertEqual(len(rules), 5)
        paths = find('shiny gold', rules, [])
        paths = sorted(paths, key=len)#print(paths)
        for p in paths:
            print( p)
        self.assertEqual(len(paths), 2)


def find(colour, rules, acc):
    containers = [r for r in rules if r[-1] == colour]
    if not containers:
        print(f'base case: {colour}, acc:{acc}')
        paths = []
        for p in acc:
            ext = [colour]
            ext.extend(p)
            paths.append(ext)       
        return paths
    
    paths = []
    #print(f'outer recursive case: acc {acc}, colour: {colour}, containers:{containers}, rules:{rules}')
    for c in containers:
        #print(f'inner recursive case: acc {acc}, colour: {colour}, container:{c}')
        if not acc:
            print(f'recursive case: not acc, colour: {colour}')
            paths += find(c[0], [r for r in rules if not r[-1] == colour], [c])
        else:
            print(f'recursive case: acc {acc}, colour: {colour}')
            for p in acc:
                ext = [colour]
                ext.extend(p)
                paths.append(p)
            paths += find(c[0], [r for r in rules if not r[-1] == colour], paths)
    print(f'recursion return: paths:{paths}')
    return paths

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

if __name__ == '__main__':
    sys.exit(main())