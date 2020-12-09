import sys
import unittest
import re

class Day8Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(('nop', 0), parse('nop +0'))
        self.assertEqual(('acc', -99), parse('acc -99'))
    
    def test_parsesample(self):
        parsefile('../_data/day8_sample.txt', True)

def parse(line, verbose=False):
    r = re.compile('(?P<cmd>(nop|acc|jmp))\s(?P<arg>[\+\-]{1}\d{1,})') 
    m = r.match(line)
    cmd, arg = m['cmd'], int(m['arg'])
    if verbose:
        print(f'{line}->({cmd}, {arg})')
    return (cmd, arg)

def parsefile(file, verbose=False):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        return [parse(line.strip(), verbose) for line in f]

def main():
    print('Day 8')

if __name__ == '__main__':
    sys.exit(main())