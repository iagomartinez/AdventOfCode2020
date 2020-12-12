import sys
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class Tests(unittest.TestCase):
    def test_parsegrid(self):
        file = '../_data/day11_smallgrid.txt'
        grid = parsegrid(file)
        prettyprint(grid)
        self.assertEqual(10, len(grid))

    def test_roundone(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid)
        print('---- after 1 round -----')
        prettyprint(newgrid)
        print('-------------------------')
        self.assertEqual([True, None, True, True, None, True, True, None, True, True], newgrid[0])
        self.assertTrue(all([seat for row in newgrid for seat in row if seat is not None]))

    def test_roundtwo(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid)
        newgrid = applyrules(newgrid)
        print('---- after 2 rounds -----')
        prettyprint(newgrid)
        print('-------------------------')

        self.assertEqual([True, None, False, False, None, False, True, None, True, True], newgrid[0])
        self.assertEqual([True, False, False, False, False, False, False, None, False, True], newgrid[1])

    def test_gridchanges_afterroundthree(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid)
        newgrid2 = applyrules(newgrid)
        newgrid3 = applyrules(newgrid2)
        print('---- after 3 rounds -----')
        prettyprint(newgrid3)
        print('-------------------------')
        self.assertNotEqual(newgrid2, newgrid3)

    def test_seatsfree_whengridstabilises(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        stablegrid = parsegrid('../_data/day11_stablegrid.txt')
        finalgrid = repeatuntilstable(grid, verbose=True)
        self.assertTrue(finalgrid, stablegrid)
        self.assertEqual(37, countoccupied(finalgrid))

    def test_comparegrids(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid)
        clone = list([list(row) for row in grid])

        self.assertFalse(equalgrids(grid, newgrid))
        self.assertTrue(equalgrids(grid, clone))

def countoccupied(grid):
    return len([seat for row in grid for seat in row if occupied(seat)])

def equalgrids(grid1, grid2):
    return all([s0 == s1 for r0,r1 in zip(grid1, grid2) for s0,s1 in zip (r0, r1)])

#   free + occupied are trivial, just for readability
def free(seat):
    return seat == False

def occupied(seat):
    return seat == True

class MaxAttemptsExceededError(Exception):
    pass

def repeatuntilstable(grid, maxattempts=100, verbose=False):
    rounds = 0
    startgrid = list([list(row) for row in grid])
    while True and rounds < maxattempts:
        newgrid = applyrules(startgrid)
        rounds += 1
        if verbose:
            print(f'---- after round {rounds} -----')
            prettyprint(newgrid)
            print('-------------------------')
        if equalgrids(startgrid, newgrid):
            if verbose:
                print(f'Grids stable after {rounds} rounds')
            return newgrid
        else:
            startgrid = list([list(row) for row in newgrid])
    raise MaxAttemptsExceededError()

def applyrules(grid, verbose=False):
    newgrid = list([list(row) for row in grid])
    for iy, seats in enumerate(grid):
        for ix, seat in enumerate(seats):
            if seat is not None:
                adjacents = checkadjacent(iy, ix, grid)
                if (free(seat) and not any(adjacents)):
                    if verbose:
                        print(f'Applied rule 1: ({iy}, {ix}) {seat}, adj: {adjacents}')
                    newgrid[iy][ix] = True
                elif (occupied(seat) and len([s for s in adjacents if occupied(s)]) >= 4):
                    if verbose:
                        print(f'Applied rule 2: ({iy}, {ix}) {seat}, adj: {adjacents}')
                    newgrid[iy][ix] = False
    return newgrid

def checkadjacent(iy, ix, grid):
    validrows = range(0, len(grid))
    validseats = range(0, len(grid[iy]))
    adjacents = [(ix - 1, iy), (ix - 1, iy -1), (ix, iy - 1), (ix + 1, iy -1), (ix + 1, iy), (ix + 1, iy + 1), (ix, iy + 1), (ix -1, iy + 1)]
    return [grid[y][x] for x, y in adjacents if x in validseats and y in validrows]

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
    startgrid = parsegrid('../_data/day11.txt')
    stablegrid = repeatuntilstable(startgrid, verbose=True)
    print(f'Stable grid found, occupied seats: {countoccupied(stablegrid)}')

if __name__ == '__main__':
    sys.exit(main())