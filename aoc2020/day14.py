import sys
import unittest
import re

class Tests(unittest.TestCase):
    def test_parsemask(self):        
        line = 'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
        mask = parsemask(line)
        self.assertEqual({34:0,29:1}, mask)

        line = 'mem[8] = 11'
        pos, value = parseinstruction(line)
        self.assertEqual((8, 11), (pos, value)) 
            
        memory = dict()
        memory[pos] = apply(mask, value)
        
        self.assertEqual(73, memory[pos])

    def test_sample(self):
        file = '../_data/day14_sample.txt'
        memory = initialise(file)
        self.assertEqual(165, sum(memory.values()))

def initialise(file):
    mask = dict()
    memory = dict()
    with open(file, 'r', newline='', encoding='utf-8') as f:
        for line in f:
            clean = line.strip()
            if clean.startswith('mask'):
                mask = parsemask(clean)
            else:
                pos, value = parseinstruction(clean)
                memory[pos] = apply(mask, value)
    return memory    

def apply(mask, value):
    tmp = list(f"{value:036b}")
    for i, v in mask.items():
        tmp[i] = str(v)
    return int(''.join(tmp), 2)

def parseinstruction(line):
    r = re.compile('mem\[(?P<pos>\d{1,})\] = (?P<val>\d{1,})')
    m = r.match(line)
    pos,value = int(m['pos']), int(m['val'])
    return pos, value

def parsemask(line):
    parsed = line.replace('mask = ', '')
    mask = dict([(ix,int(val)) for ix, val in enumerate(parsed) if val != 'X'])
    return mask

def main():
    print('----------- day14 -----------')
    memory = initialise('../_data/day14.txt')
    print(f'Sum of values in memory is {sum(memory.values())}')

if __name__ == '__main__':
    sys.exit(main())