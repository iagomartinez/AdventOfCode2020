import sys
import unittest
import re

class AOCTests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(('nop', 0), parse('nop +0'))
        self.assertEqual(('acc', -99), parse('acc -99'))
    
    def test_parsesample(self):
        commands = parsefile('../_data/day8_sample.txt')
        self.assertEqual(9, len(commands))

    def test_commands(self):
        rt = BootCodeRunTime([parse('nop +0'), parse('acc +99'), parse('jmp +2'), parse('nop +0'), parse('acc -57')], True)
        for acc in rt.next():
            print(acc)
        self.assertEqual(42, rt.acc)
        self.assertEqual([('nop', 0), ('acc', 99), ('jmp', 2), ('acc', -57)], rt.stack)


class BootCodeRunTime():
    def __init__(self, program, verbose=False):
        self.program = program
        self.acc = 0
        self.stack = []
        self.pointer = 0
        self.v = verbose
        self.map = {'nop':self.__nop, 'acc': self.__acc, 'jmp': self.__jmp}

    def __nop(self, arg):
        self.pointer += 1
        return None
    
    def __acc(self, arg):
        self.acc += arg
        self.pointer += 1

    def __jmp(self, arg):
        self.pointer += arg

    def next(self):
        while self.pointer < len(self.program):
            cmd, arg = self.program[self.pointer]
            self.map[cmd](arg)
            self.stack.append((cmd, arg))
            if self.v:
                print(f'cmd: {cmd}, arg: {arg}, pointer: {self.pointer}')
            yield self.acc
    
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