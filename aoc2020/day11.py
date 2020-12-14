import sys
import unittest
import time
import functools
unittest.TestLoader.sortTestMethodsUsing = None

class Tests(unittest.TestCase):
    def test_parsegrid(self):
        file = '../_data/day11_smallgrid.txt'
        grid = parsegrid(file)
        prettyprint(grid)
        self.assertEqual(10, len(grid))

    def test_seatsfree_whengridstabilises(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        stablegrid = parsegrid('../_data/day11_stablegrid.txt')
        finalgrid,_ = repeatuntilstable(grid, verbose=True)
        self.assertTrue(finalgrid, stablegrid)
        self.assertEqual(26, countoccupied(finalgrid))

    def test_comparegrids(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        scanner = VisibleSeatsScanner(grid)
        newgrid = applyrules(grid, scanner, True)
        clone = list([list(row) for row in grid])
        self.assertFalse(equalgrids(grid, newgrid))
        self.assertTrue(equalgrids(grid, clone))

    def test_lineofsight_onsmallgrid(self):
        scanner = VisibleSeatsScanner(parsegrid('../_data/day11_smallgrid.txt'))
        seen = scanner.scan(0, 9)
        print(seen)
        self.assertEqual(3, len(seen))        

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
    scanner = VisibleSeatsScanner(grid)
    while True and rounds < maxattempts:
        newgrid = applyrules(startgrid, scanner)
        rounds += 1
        if verbose:
            print(f'---- after round {rounds} -----')
            prettyprint(newgrid)
            print('-------------------------')
        if equalgrids(startgrid, newgrid):
            return (newgrid, rounds)
        else:
            startgrid = list([list(row) for row in newgrid])
    raise MaxAttemptsExceededError()

def applyrules(grid, scanner, verbose=False):
    newgrid = list([list(row) for row in grid])
    for iy, seats in enumerate(grid):
        for ix, seat in enumerate(seats):
            if seat is not None:
                visibleseats = [grid[y][x] for (y,x) in scanner.scan(iy, ix)]
                if verbose:
                    print(f'Scanning, {iy},{ix}, visible: {visibleseats}')
                if (free(seat) and not any([occupied(seat) for seat in visibleseats])):
                    if verbose:
                        print(f'Applied rule 1: ({iy}, {ix}) {seat}, adj: {visibleseats}')
                    newgrid[iy][ix] = True
                elif (occupied(seat) and len([s for s in visibleseats if occupied(s)]) >= 5):
                    if verbose:
                        print(f'Applied rule 2: ({iy}, {ix}) {seat}, adj: {visibleseats}')
                    newgrid[iy][ix] = False
    return newgrid

class VisibleSeatsScanner():
    def __init__(self, grid, verbose=False):
        self.grid = grid
        self.v = verbose

    def __row(self, startx, endx, row, step=1):
        if startx in range(0, len(self.grid[row])):
            for x in range(startx, endx, step):
                if self.grid[row][x] is not None:
                    return (row, x)
        return None

    def __col(self, starty, endy, col, step=1):
        if starty in range(0, len(self.grid)):
            for y in range(starty, endy, step):
                if self.grid[y][col] is not None:
                    return (y, col)
        return None

    def __diagonal(self, starty, startx, ystep, xstep):
        ypos, xpos = starty + ystep, startx + xstep
        while xpos in range(0, len(self.grid[starty]))  and ypos in range(0, len(self.grid)):
            if self.grid[ypos][xpos] is not None:
                return (ypos, xpos)
            ypos += ystep
            xpos += xstep
        return None

    @functools.lru_cache(maxsize=1000)
    def scan(self, ypos, xpos):
        seen = set()
        seen.add(self.__row(xpos-1,-1,ypos,step=-1))
        seen.add(self.__row(xpos+1,len(self.grid[ypos]),ypos))
        seen.add(self.__col(ypos-1,-1,xpos,step=-1))
        seen.add(self.__col(ypos+1,len(self.grid),xpos))
        seen.add(self.__diagonal(ypos,xpos,1,1))
        seen.add(self.__diagonal(ypos,xpos,-1,1))
        seen.add(self.__diagonal(ypos,xpos,1,-1))
        seen.add(self.__diagonal(ypos,xpos,-1,-1))
        return {pos for pos in seen if pos is not None}

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
    charmap = {'#':True, 'L':False}
    with open(file, 'r', newline='', encoding='utf-8') as f:
        for line in f:
            row = [None if c == '.' else charmap[c] for c in line.strip()]
            grid.append(row)
    return grid

def main():
    print('---------- Day 11 ----------')
    startgrid = parsegrid('../_data/day11.txt')
    t0 = time.perf_counter()
    stablegrid, rounds = repeatuntilstable(startgrid)
    t1 = time.perf_counter()
    print(f'Stable grid found after {rounds} rounds, occupied seats: {countoccupied(stablegrid)} in {t1 - t0:0.4f} seconds')

if __name__ == '__main__':
    sys.exit(main())