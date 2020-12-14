import sys
import unittest
import re

class Tests(unittest.TestCase):
    def test_parseinstruction(self):
        action, value = parse('F10')
        self.assertEqual(('F', 10), (action,value))       

    def test_shipmoves(self):
        action, value = parse('F10')
        ship = Ship()
        endpos = ship.move(action, value)
        self.assertEqual((0, 10,'E'), endpos)

    def test_manhattandistance(self):
        action, value = parse('F10')
        ship = Ship()
        ship.move(action, value)     
        self.assertEqual(10, ship.manhattandistance())

class Ship():
    def __init__(self, verbose=False):
        self.position = (0, 0, 'E')
        self.v = verbose
        self.log = [self.position]

    def move(self, action, value):
        latitude,longitude,direction = self.position
        if action == 'F':
            if direction == 'E':
                self.position = latitude, longitude + value, direction
                self.log.append(self.position)
        return self.position
        
    def manhattandistance(self):
        lat0,long0,_ = self.log[0]
        lat1,long1,_ = self.log[-1]
        return (lat1-lat0 + long1-long0)

def parse(instruction):
    r = re.compile('(?P<action>(N|S|E|W|L|R|F))(?P<value>\d{1,})') 
    m = r.match(instruction)
    action, value = m['action'], int(m['value']) 
    return action, value

def main():
    print('----------- day12 -----------')

if __name__ == '__main__':
    sys.exit(main())