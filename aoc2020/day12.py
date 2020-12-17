import sys
import unittest
import re
from parameterized import parameterized

class Tests(unittest.TestCase):
    def test_parseinstruction(self):
        action, value = parse('F10')
        self.assertEqual(('F', 10), (action,value))

    @parameterized.expand([
        ('F10', (10, 100), (11, 110)),
        ('N3', (0, 0), (4, 10)),
        ('S3', (0, 0), (-2, 10)),
        ('E3', (0, 0), (1, 13)),
        ('W3', (0, 0), (1, 7)),
        ('R90', (0, 0), (-10,1)),
        ('L90', (0, 0), (10, -1)),
        ('R270', (0, 0), (10, -1)),
        ('L270', (0, 0), (-10, 1)),
        ('R360', (0, 0), (1, 10)),
        ('L360', (0, 0), (1, 10)),
        ('L180', (0, 0), (-1, -10)),
        ('R180', (0, 0), (-1, -10)),
    ])
    def test_navigation(self, instruction,expectedposition, expectedwaypoint):
        action, value = parse(instruction)
        navigator = Navigator(True)
        endpos = navigator.move(action, value)
        self.assertEqual(expectedposition, endpos)
        self.assertEqual(navigator.waypoint.position(), expectedwaypoint)

    def test_sample(self):
        file = '../_data/day12_sample.txt'
        _, distance = sail(file)
        self.assertEqual(286, distance)

class WayPoint():
    def __init__(self, latitude, longitude, verbose=False):
        self.relativelat = 1
        self.relativelong = 10
        self.setrelativeto(latitude, longitude)
        self.directionmap = {0:(1,-1), 90:(1,1), 180:(-1,1), 270:(-1,-1)}
        self.v = verbose

    def position(self):
        return (self.absolutelat, self.absolutelong)

    def rotate(self, rotation, latitude, longitude):        
        steps = abs(rotation) // 90
        rotationstep = rotation // steps

        rotatedlat = self.relativelat
        rotatedlong = self.relativelong
        for _ in range(steps):
            # switch lat and long
            if rotation > 0:
                tmplat = rotatedlong * -1
                tmplong = rotatedlat
            else:
                tmplat = rotatedlong
                tmplong = rotatedlat * -1
            rotatedlat, rotatedlong = tmplat, tmplong
            if self.v:
                print(f'in rotate: {rotatedlat}, {rotatedlong}')

        if self.v:
            print(f'{self.relativelat}, {self.relativelong} -> rotate {rotation} ->  {rotatedlat}, {rotatedlong}')
        self.relativelat = rotatedlat
        self.relativelong = rotatedlong
        self.setrelativeto(latitude, longitude)

    def movelat(self, units):
        self.relativelat += units
        self.absolutelat += units

    def movelong(self, units):
        self.relativelong += units
        self.absolutelong += units

    def plotrelativeto(self, startlatitude, startlongitude, units):
        newlat, newlong = startlatitude + units * self.relativelat, startlongitude + units * self.relativelong
        if self.v:
            print(f'{startlatitude} + {units * self.relativelat}, {startlongitude} + {units * self.relativelong} ->  {newlat}, {newlong}')
        self.setrelativeto(newlat, newlong)
        return(newlat, newlong)

    def setrelativeto(self, latitude, longitude):
        self.absolutelat = latitude + self.relativelat
        self.absolutelong = longitude + self.relativelong

class Navigator():
    def __init__(self, verbose=False):
        self.latitude = 0
        self.longitude = 0
        self.v = verbose
        self.waypoint = WayPoint(self.latitude, self.longitude, verbose=verbose)
        self.log = [(self.latitude, self.longitude)]

    def __turn(self, rotation):
        self.waypoint.rotate(rotation, self.latitude, self.longitude)

    def __forward(self, units):
        newlat, newlong = self.waypoint.plotrelativeto(self.latitude, self.longitude, units)
        self.latitude, self.longitude = newlat, newlong
        self.log.append((self.latitude, self.longitude))

    def move(self, action, value):
        if action in {'R', 'L'}:
            rotation = -value if action == 'L' else value
            self.__turn(rotation)
        if action == 'F':
            self.__forward(value)
        if action in {'N', 'S'}:
            self.waypoint.movelat(-value if action == 'S' else value)
        if action in {'E', 'W'}:
            self.waypoint.movelong(-value if action == 'W' else value)
        return self.latitude, self.longitude

    def manhattandistance(self):
        lat0,long0 = self.log[0]
        lat1,long1 = self.log[-1]
        return (abs(lat1-lat0) + abs(long1-long0))

def sail(commands, verbose=False):
    with open(commands, 'r', newline='', encoding='utf-8') as f:
        instructions = [parse(line.strip()) for line in f]
    nav = Navigator(verbose=verbose)
    for action,value in instructions:
        newpos = nav.move(action, value)
        if verbose:
            print(f'{action},{value} -> {newpos}, waypoint: ({nav.waypoint.relativelat}, {nav.waypoint.relativelong}), distance: {nav.manhattandistance()}')
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