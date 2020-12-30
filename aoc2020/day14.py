import sys
import unittest
import re

class Tests(unittest.TestCase):
    def test_parsemask(self):        
        line = 'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
        mask = ChipEmulator.parsemask(line)
        self.assertEqual({34:0,29:1}, mask)

        line = 'mem[8] = 11'
        pos, value = ChipEmulator.parseinstruction(line)
        self.assertEqual((8, 11), (pos, value)) 
            
        memory = dict()
        memory[pos] = ChipEmulator.apply_v1(mask, value)
        
        self.assertEqual(73, memory[pos])

    def test_sample(self):
        file = '../_data/day14_sample.txt'
        em = ChipEmulator()
        memory = em.initialise_v1(file)
        self.assertEqual(165, sum(memory.values()))

class ChipEmulator():
    def __init__(self):
        self.memory = dict()

    @staticmethod
    def parseinstruction(line):
        r = re.compile('mem\[(?P<pos>\d{1,})\] = (?P<val>\d{1,})')
        m = r.match(line)
        pos,value = int(m['pos']), int(m['val'])
        return pos, value

    @staticmethod
    def parsemask(line):
        parsed = line.replace('mask = ', '')
        mask = dict([(ix,int(val)) for ix, val in enumerate(parsed) if val != 'X'])
        return mask

    @staticmethod
    def apply_v1(mask, value):
        tmp = list(f"{value:036b}")
        for i, v in mask.items():
            tmp[i] = str(v)
        return int(''.join(tmp), 2)  

    def initialise_v1(self, file):
        mask = dict()
        with open(file, 'r', newline='', encoding='utf-8') as f:
            for line in f:
                clean = line.strip()
                if clean.startswith('mask'):
                    mask = ChipEmulator.parsemask(clean)
                else:
                    pos, value = ChipEmulator.parseinstruction(clean)
                    self.memory[pos] = ChipEmulator.apply_v1(mask, value)
        return self.memory  


def main():
    print('----------- day14 -----------')
    em = ChipEmulator()
    memory = em.initialise_v1('../_data/day14.txt')
    print(f'Sum of values in memory is {sum(memory.values())}')

if __name__ == '__main__':
    sys.exit(main())