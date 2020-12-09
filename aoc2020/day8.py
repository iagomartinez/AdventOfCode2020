import sys
import unittest
import re

class AOCTests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(('nop', 0), parse('nop +0'))
        self.assertEqual(('acc', -99), parse('acc -99'))
    
    def test_sampleprogram(self):
        commands = parsefile('../_data/day8_sample.txt')
        self.assertEqual(9, len(commands))
        rt = BootCodeRunTime(commands, True)
        with self.assertRaises(InfiniteLoopError) as il:
            for _ in rt.next():
                pass
        self.assertEqual(5, il.exception.acc)

    def test_commands(self):
        rt = BootCodeRunTime([parse('nop +0'), parse('acc +99'), parse('jmp +2'), parse('nop +0'), parse('acc -57')], True)
        for acc in rt.next():
            print(acc)
        self.assertEqual(42, rt.acc)
        self.assertEqual([(0, 'nop', 0), (1, 'acc', 99), (2, 'jmp', 2), (4, 'acc', -57)], rt.stack)

class BootCodeRunTime():
    def __init__(self, program, verbose=False):
        self.program = program
        self.acc = 0
        self.stack = []
        self.pointer = 0
        self.v = verbose
        self.execute = {'nop':self.__nop, 'acc': self.__acc, 'jmp': self.__jmp}

    def __nop(self, arg):
        return 1
    
    def __acc(self, arg):
        self.acc += arg
        return 1

    def __jmp(self, arg):
        return arg

    def next(self):
        while self.pointer < len(self.program):
            cmd, arg = self.program[self.pointer]
            if (self.pointer, cmd, arg) in self.stack:
                raise InfiniteLoopError(self.acc)
            increment = self.execute[cmd](arg)
            self.stack.append((self.pointer, cmd, arg))
            self.pointer += increment
            if self.v:
                print(f'cmd: {cmd}, arg: {arg}, acc: {self.acc}, next: {self.pointer}')
            yield self.acc

class InfiniteLoopError(Exception):
    def __init__(self, acc):
        self.acc = acc

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
    print('------- Day 8 ---------')
    rt = BootCodeRunTime(parsefile('../_data/day8.txt'), True)
    try:
        for _ in rt.next():
            pass
    except InfiniteLoopError as il:
        print(f'Infinite loop detected! acc: {il.acc}')

if __name__ == '__main__':
    sys.exit(main())