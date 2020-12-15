import sys
import unittest
import re
from parameterized import parameterized

class Tests(unittest.TestCase):
    def test_parseinstruction(self):
        action, value = parse('F10')
        self.assertEqual(('F', 10), (action,value))       

    @parameterized.expand([
        ('F10', (0, 10, 270), 10),
        ('N10', (10, 0, 270), 10),
        ('S10', (-10, 0, 270), 10),
        ('E10', (0, 10, 270), 10),
        ('W10', (0, -10, 270), 10),
        ('R90', (0, 0, 0), 0),
        ('R180', (0, 0, 90), 0),
        ('R270', (0, 0, 180), 0),
        ('R360', (0, 0, 270), 0),
        ('L90', (0, 0, 180), 0),
        ('L180', (0, 0, 90), 0),
        ('L270', (0, 0, 0), 0),
        ('L360', (0, 0, 270), 0)
    ])
    def test_navigation(self, instruction,expectedposition, expecteddistance):
        action, value = parse(instruction)
        navigator = Navigator()
        endpos = navigator.move(action, value)
        self.assertEqual(expectedposition, endpos)
        self.assertEqual(expecteddistance, navigator.manhattandistance())

class Navigator():
    def __init__(self, verbose=False):
        self.position = (0, 0, 270)
        self.v = verbose
        self.log = [self.position]

    def move(self, action, value):
        latitude,longitude,direction = self.position
        if action in {'R', 'L'}:
            direction = ((direction - value) if action == 'L' else (direction + value)) % 360
            self.position = latitude, longitude, direction
        if action == 'F':
            if direction == 270:
                self.position = latitude, longitude + value, direction
                self.log.append(self.position)
        if action in {'N', 'S'}:
            self.position =  (latitude - value) if action == 'S' else (latitude + value), longitude, direction 
            self.log.append(self.position)
        if action in {'E', 'W'}:
            self.position = latitude, (longitude - value) if action == 'W' else (latitude + value), direction
            self.log.append(self.position)
        return self.position
        
    def manhattandistance(self):
        lat0,long0,_ = self.log[0]
        lat1,long1,_ = self.log[-1]
        return (abs(lat1-lat0) + abs(long1-long0))

def parse(instruction):
    r = re.compile('(?P<action>(N|S|E|W|L|R|F))(?P<value>\d{1,})') 
    m = r.match(instruction)
    action, value = m['action'], int(m['value']) 
    return action, value

def main():
    print('----------- day12 -----------')

if __name__ == '__main__':
    sys.exit(main())