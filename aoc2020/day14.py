import sys
import unittest
import re
from parameterized import parameterized

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

    def test_applyv2(self):
        line = 'mask = 000000000000000000000000000000X1001X'
        mask = ChipEmulator.parsemask_v2(line)
        self.assertEqual({35:'X',34:'1',31:'1',30:'X'}, mask)

        line = 'mem[42] = 100'
        pos, value = ChipEmulator.parseinstruction(line)
        self.assertEqual({(26, 100), (27, 100), (58, 100), (59, 100)}, ChipEmulator.apply_v2(mask, pos, value))

    @parameterized.expand([
        ('mask = 00000000000000000000000000000000001X', 'mem[2] = 100', {(3, 100), (2, 100)}),
        ('mask = X00000000000000000000000000000000000', 'mem[0] = 100', {(0, 100), (34359738368, 100)}),
    ])
    def test_apply_cases(self, mask, line, expected):        
        mask = ChipEmulator.parsemask_v2(mask)
        pos, value = ChipEmulator.parseinstruction(line)
        self.assertEqual(expected, ChipEmulator.apply_v2(mask, pos, value))

    def test_sample(self):
        file = '../_data/day14_sample.txt'
        em = ChipEmulator()
        memory = em.initialise_v1(file)
        self.assertEqual(165, sum(memory.values()))

    def test_floating_sample(self):
        file = '../_data/day14_floating.txt'
        em = ChipEmulator()
        memory = em.initialise_v2(file, True)
        self.assertEqual(208, sum(memory.values()))
        print(memory)

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
    def parsemask_v2(line):
        parsed = line.replace('mask = ', '')
        return dict([(ix,val) for ix, val in enumerate(parsed) if val != '0'])

    @staticmethod
    def apply_v1(mask, value):
        tmp = list(f"{value:036b}")
        for i, v in mask.items():
            tmp[i] = str(v)
        return int(''.join(tmp), 2)

    @staticmethod
    def apply_rec(mask, baseref, addresses, verbose=False):
        def newref(baseref, pos, bitval): 
            new = list(f"{baseref:036b}")
            new[pos] = bitval
            if verbose:
                print(f"{baseref}[{pos}]={bitval}:{baseref:036b} -> {int(''.join(new), 2)}:{''.join(new)}")
            return int(''.join(new), 2)

        if not mask:
            return addresses
        pos, op = mask[0]
        if verbose:
            print(f'in recursive case, mask={mask}, addresses={len(addresses)}')
        if op == 'X':
            newset = set()
            if addresses:
                for a in addresses:
                    newset.add(newref(a, pos, '0'))
                    newset.add(newref(a, pos, '1'))
            else:
                newset.add(newref(baseref, pos, '0'))
                newset.add(newref(baseref, pos, '1'))
            addresses = newset
        return ChipEmulator.apply_rec(mask[1:], baseref, addresses, verbose)

    @staticmethod
    def apply_v2(mask, baseref, value, verbose=False):
        mask = list(mask.items())

        asbits = list(f"{baseref:036b}")
        for pos in [p for p,op in mask if op == '1']:
            asbits[pos] = '1'

        addresses = ChipEmulator.apply_rec([(p,op) for p,op in mask if op == 'X'], int(''.join(asbits), 2), set(), verbose)
        return {(a, value) for a in addresses}   

    def initialise_v2(self, file, verbose=False):
        self.memory = dict()
        print(f'starting initialise: {self.memory}')
        mask = dict()
        newmasks = 0
        ops = 0
        addresscount = 0
        with open(file, 'r', newline='', encoding='utf-8') as f:
            for line in f:
                clean = line.strip()
                if clean.startswith('mask'):
                    mask = ChipEmulator.parsemask_v2(clean)
                    newmasks += 1
                else:
                    pos, value = ChipEmulator.parseinstruction(clean)
                    newrefs = ChipEmulator.apply_v2(mask, pos, value, verbose)
                    addresscount += len(newrefs)
                    for address, value in newrefs:
                        if address >= (2 ** 36 - 1):
                            print(f'accessing address out of bounds: {address}')
                        self.memory[address] = value
                    ops += 1
                    if len(newrefs) != 2**len([1 for e in mask.values() if e == 'X']):
                        print(f"Expected {2**len([1 for e in mask.values() if e == 'X'])}, applied {len(newrefs)}")
        if verbose:
            print(f'total memory entries: {len(self.memory)}, masks: {newmasks}, ops applied: {ops}, addresses: {addresscount}')         
        return self.memory

    def initialise_v1(self, file):
        self.memory = dict()
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
    print(f'Sum of memory using v1 emulator is {sum(memory.values())}')
    memory = em.initialise_v2('../_data/day14.txt')
    print(f'Sum of memory using v2 emulator is {sum(memory.values())}')

if __name__ == '__main__':
    sys.exit(main())