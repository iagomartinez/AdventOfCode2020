import sys
import unittest
import re

class AOCTests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(('nop', 0), parse('nop +0'))
        self.assertEqual(('acc', -99), parse('acc -99'))

    def test_parsefile(self):
        commands = parseprogram('../_data/day8_sample.txt')
        self.assertEqual(9, len(commands))
    
    def test_sampleprogram(self):
        program = parseprogram('../_data/day8_sample.txt')
        rt = BootCodeRunTime(program)
        with self.assertRaises(InfiniteLoopError) as il:
            rt.execute()
        ex = il.exception
        self.assertEqual(5, ex.acc)
        print(f'Attempted duplicate instruction cmd: {ex.cmd}, arg: {ex.arg}, pointer: {ex.pointer}')

    def test_fixedprogramcompletes(self):
        program = parseprogram('../_data/day8_sample.txt')
        cmd, arg = program[7]
        cmd = 'nop'
        program[7] = cmd, arg    
        rt = BootCodeRunTime(program)
        acc = rt.execute()
        self.assertEqual(8, acc)

    def test_commands(self):
        program = [parse('nop +0'), parse('acc +99'), parse('jmp +2'), parse('nop +0'), parse('acc -57')]
        rt = BootCodeRunTime(program, True)
        acc = rt.execute()
        self.assertEqual(42, acc)
        self.assertEqual([(0, 'nop', 0), (1, 'acc', 99), (2, 'jmp', 2), (4, 'acc', -57)], rt.stack)

class BootCodeRunTime():
    def __init__(self, program, verbose=False):
        self.acc = 0
        self.stack = []
        self.pointer = 0
        self.v = verbose
        self.program = program
        self.run = {'nop':self.__nop, 'acc': self.__acc, 'jmp': self.__jmp}

    def __nop(self, arg):
        return 1
        
    def __acc(self, arg):
        self.acc += arg
        return 1

    def __jmp(self, arg):
        return arg

    def __next(self):
        while self.pointer < len(self.program):
            cmd, arg = self.program[self.pointer]
            if (self.pointer, cmd, arg) in self.stack:
                raise InfiniteLoopError(self.acc, self.stack, cmd, arg, self.pointer)
            increment = self.run[cmd](arg)
            self.stack.append((self.pointer, cmd, arg))
            self.pointer += increment
            if self.v:
                print(f'cmd: {cmd}, arg: {arg}, acc: {self.acc}, next: {self.pointer}')
            yield self.acc

    def execute(self):
        for _ in self.__next():
            pass
        return self.acc

class InfiniteLoopError(Exception):
    def __init__(self, acc, stack, cmd, arg, pointer):
        self.acc, self.stack, self.cmd, self.arg, self.pointer = acc, stack, cmd, arg, pointer

def parse(line, verbose=False):
    r = re.compile('(?P<cmd>(nop|acc|jmp))\s(?P<arg>[\+\-]{1}\d{1,})') 
    m = r.match(line)
    cmd, arg = m['cmd'], int(m['arg'])
    if verbose:
        print(f'{line}->({cmd}, {arg})')
    return (cmd, arg)

def parseprogram(file, verbose=False):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        return [parse(line.strip(), verbose) for line in f]

def main():
    print('------- Day 8 ---------')
    program = parseprogram('../_data/day8.txt')
    rt = BootCodeRunTime(program, True)
    try:
        rt.execute()
    except InfiniteLoopError as il:
        print(f'Infinite loop detected! acc: {il.acc}')
        print(f'Attempted duplicate instruction: cmd: {il.cmd}, arg: {il.arg}, pointer: {il.pointer}')
        
if __name__ == '__main__':
    sys.exit(main())