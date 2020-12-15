import sys
import unittest
import re
from parameterized import parameterized

class Tests(unittest.TestCase):
    def test_parseinstruction(self):
        action, value = parse('F10')
        self.assertEqual(('F', 10), (action,value))       

    @parameterized.expand([
        ('F10', (0, 10, 90), 10),
        ('N10', (10, 0, 90), 10),
        ('S10', (-10, 0, 90), 10),
        ('E10', (0, 10, 90), 10),
        ('W10', (0, -10, 90), 10),
        ('R90', (0, 0, 180), 0),
        ('R180', (0, 0, 270), 0),
        ('R270', (0, 0, 0), 0),
        ('R360', (0, 0, 90), 0),
        ('L90', (0, 0, 0), 0),
        ('L180', (0, 0, 270), 0),
        ('L270', (0, 0,180), 0),
        ('L360', (0, 0, 90), 0)
    ])
    def test_navigation(self, instruction,expectedposition, expecteddistance):
        action, value = parse(instruction)
        navigator = Navigator()
        endpos = navigator.move(action, value)
        self.assertEqual(expectedposition, endpos)
        self.assertEqual(expecteddistance, navigator.manhattandistance())

    def test_sample(self):
        file = '../_data/day12_sample.txt'
        _, distance = sail(file)
        self.assertEqual(25, distance)

class Navigator():
    def __init__(self, verbose=False):
        self.position = (0, 0, 90)
        self.v = verbose
        self.log = [self.position]
        self.directionmap = {0:1, 90:1, 180:-1, 270:-1}

    def move(self, action, value):
        latitude,longitude,direction = self.position
        if action in {'R', 'L'}:
            direction = ((direction - value) if action == 'L' else (direction + value)) % 360
            self.position = latitude, longitude, direction
        if action == 'F':
            distance = value * self.directionmap[direction]
            if direction in {90, 270}:
                self.position = latitude, longitude + distance, direction
            if direction in {0, 180}:
                self.position = latitude + distance, longitude, direction                
            self.log.append(self.position)
        if action in {'N', 'S'}:
            self.position =  (latitude - value) if action == 'S' else (latitude + value), longitude, direction 
            self.log.append(self.position)
        if action in {'E', 'W'}:
            self.position = latitude, (longitude - value) if action == 'W' else (longitude + value), direction
            self.log.append(self.position)
        return self.position
        
    def manhattandistance(self):
        lat0,long0,_ = self.log[0]
        lat1,long1,_ = self.log[-1]
        return (abs(lat1-lat0) + abs(long1-long0))

def sail(commands):
    with open(commands, 'r', newline='', encoding='utf-8') as f:
        instructions = [parse(line.strip()) for line in f]
    nav = Navigator()
    for action,value in instructions:
        newpos = nav.move(action, value)
        print(f'{action},{value} -> {newpos}, distance: {nav.manhattandistance()}')
    return newpos, nav.manhattandistance()

def parse(instruction):
    r = re.compile('(?P<action>(N|S|E|W|L|R|F))(?P<value>\d{1,})') 
    m = r.match(instruction)
    action, value = m['action'], int(m['value']) 
    return action, value

def main():
    print('----------- day12 -----------')
    finalpos, manhattandistance = sail('../_data/day12.txt')
    print(f'final position: {finalpos}, Manhattan distance: {manhattandistance}')

if __name__ == '__main__':
    sys.exit(main())