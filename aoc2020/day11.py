import sys
import unittest

class Tests(unittest.TestCase):
    def test_parsegrid(self):
        file = '../_data/day11_smallgrid.txt'
        grid = parsegrid(file)
        prettyprint(grid)
        self.assertEqual(10, len(grid))

    def test_firstround(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid)
        prettyprint(newgrid)
        self.assertEqual([True, None, True, True, None, True, True, None, True, True], newgrid[0])
        self.assertTrue(all([seat for row in newgrid for seat in row if seat is not None]))

def applyrules(grid):
    newgrid = list([list(row) for row in grid])
    validrows = range(-len(grid), len(grid))
    for iy, seats in enumerate(grid):
        validseats = range(-len(seats), len(seats))
        for ix, seat in enumerate(seats):
            adjacents = [(ix - 1, iy), (ix - 1, iy -1), (ix, iy - 1), (ix + 1, iy -1), (ix + 1, iy), (ix + 1, iy + 1), (ix, iy + 1), (ix -1, iy + 1)]
            if (seat is not None and not any([grid[y][x] for x, y in adjacents if x in validseats and y in validrows])):
                newgrid[iy][ix] = True
    return newgrid

def prettyprint(grid):
    charmap = {True:'#', False:'L'}
    for row in grid:
        for seat in row:
            symbol = '.' if seat is None else charmap[seat]
            print(f'{symbol}', end='')
        print('')

def parsegrid(file):
    grid = []
    with open(file, 'r', newline='', encoding='utf-8') as f:        
        for line in f:
            row = [False if c == 'L' else None for c in line.strip()]
            grid.append(row)
    return grid
    
def main():
    print('---------- Day 11 ----------')

if __name__ == '__main__':
    sys.exit(main())