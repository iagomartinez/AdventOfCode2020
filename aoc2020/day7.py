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
        with open('../_data/day7_sample.txt', 'r', newline='', encoding='utf-8') as f:
            rules = [r for line in f for r in parse(line, True) ]        
        self.assertEqual(len(rules), 15)

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