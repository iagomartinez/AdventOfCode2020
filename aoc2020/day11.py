import sys
import unittest
import time
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
        finalgrid = repeatuntilstable(grid, verbose=True)
        self.assertTrue(finalgrid, stablegrid)
        self.assertEqual(26, countoccupied(finalgrid))

    def test_comparegrids(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid, True)
        clone = list([list(row) for row in grid])
        self.assertFalse(equalgrids(grid, newgrid))
        self.assertTrue(equalgrids(grid, clone))

    def test_scandiagonal(self):
        grid = parsegrid('../_data/day11_los.txt')
        seatpos = scandiagonal(grid, 4,3,1,1)
        self.assertEqual((5,4), seatpos)
        seatpos = scandiagonal(grid, 4,3,-1,1)
        self.assertEqual((0,7), seatpos)
        seatpos = scandiagonal(grid, 4,3,1,-1)
        self.assertEqual((7,0), seatpos)
        seatpos = scandiagonal(grid, 4, 3,-1,-1)
        self.assertEqual((2,1), seatpos)

    def test_lineofsight_onsmallgrid(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        seen = checklineofsight(0, 9, grid, True)
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
                visibleseats = [grid[y][x] for y,x in checklineofsight(iy, ix, grid)]
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

def scanrow(grid, startx, endx, row, step=1):
    if startx in range(0, len(grid[row])):
        for x in range(startx, endx, step):
            if grid[row][x] is not None:
                return (row, x)
    return None

def scancol(grid, starty, endy, col, step=1):
    if starty in range(0, len(grid)):
        for y in range(starty, endy, step):
            if grid[y][col] is not None:
                return (y, col)
    return None

def scandiagonal(grid, starty, startx, ystep, xstep, verbose=False):
    ypos, xpos = starty + ystep, startx + xstep
    while xpos in range(0, len(grid[starty]))  and ypos in range(0, len(grid)):
        if grid[ypos][xpos] is not None:
            return (ypos, xpos)
        ypos += ystep
        xpos += xstep
    return None

def checklineofsight(row, col, grid, verbose=False):
    seen = set()
    seen.add(scanrow(grid,col-1,-1,row,step=-1))
    seen.add(scanrow(grid,col+1,len(grid[row]),row))
    seen.add(scancol(grid,row-1,-1,col,step=-1))
    seen.add(scancol(grid,row+1,len(grid),col))
    seen.add(scandiagonal(grid,row,col,1,1, verbose))
    seen.add(scandiagonal(grid,row,col,-1,1, verbose))
    seen.add(scandiagonal(grid,row,col,1,-1, verbose))
    seen.add(scandiagonal(grid,row,col,-1,-1, verbose))
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
    stablegrid = repeatuntilstable(startgrid)
    t1 = time.perf_counter()
    print(f'Stable grid found, occupied seats: {countoccupied(stablegrid)} in {t1 - t0:0.4f} seconds')

if __name__ == '__main__':
    sys.exit(main())