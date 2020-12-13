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
        finalgrid = repeatuntilstable(grid)
        self.assertTrue(finalgrid, stablegrid)
        self.assertEqual(37, countoccupied(finalgrid))

    def test_comparegrids(self):
        grid = parsegrid('../_data/day11_smallgrid.txt')
        newgrid = applyrules(grid)
        clone = list([list(row) for row in grid])

        self.assertFalse(equalgrids(grid, newgrid))
        self.assertTrue(equalgrids(grid, clone))

    def test_scandiagonal(self):
        grid = parsegrid('../_data/day11_los.txt')
        seatpos = scandiagonal(grid, 4, 3,1,1)
        self.assertEqual((5,4), seatpos)
        seatpos = scandiagonal(grid, 4, 3,-1,1)
        self.assertEqual((2,1), seatpos)
        seatpos = scandiagonal(grid, 4, 3,1,-1)
        self.assertEqual((7,0), seatpos)
        seatpos = scandiagonal(grid, 4, 3,-1,-1)
        self.assertEqual((0,7), seatpos)

    def test_lineofsight(self):
        grid = parsegrid('../_data/day11_los.txt')
        seen = checklineofsight(4, 3, grid)
        self.assertEqual({(4,2),(4,8),(1,3),(8,3),(5,4),(2,1),(7,0),(0,7)}, seen)

    def test_flatvs2d(self):
        grid = [[1,2,3],[4,5,6],[7,8,9]]
        starty, startx = 1,1
        flat = [item for row in grid for item in row]
        flatindex = starty * len(grid) + startx
        self.assertEqual(flat[flatindex], 5)
        self.assertEqual(4, flatindex)
        gridy = flatindex // len(grid)
        gridx = flatindex % len(grid[gridy])
        self.assertEqual((gridy, gridx), (1,1))

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

def scanrow(grid, startx, endx, row, step=1):
    for x in range(startx, endx, step):
        print(f'{row}, {x}, {grid[row][x]}')
        if grid[row][x] is not None:
            return (row, x)
    return None

def scancol(grid, starty, endy, col, step=1):
    for y in range(starty, endy, step):
        print(f'{y}, {col}, {grid[y][col]}')
        if grid[y][col] is not None:
            return (y, col)
    return None

def scandiagonal(grid, starty, startx, direction, modifier):
    flatgrid = [item for row in grid for item in row]
    flatindex = starty * len(grid) + startx
    print(f'Scanning diagonal - start index: {flatindex}')
    if direction == -1:
        end = -1
    else:
        end = len(flatgrid)+1
    step = direction * (len(grid[starty])+modifier)
    for index in range(flatindex+step, end, step):    
        gridy = index // len(grid)
        gridx = index % len(grid[gridy])
        print(f'Scanning index: {index} = ({gridy},{gridx})=>{flatgrid[index]}')
        if flatgrid[index] is not None:
            return (gridy, gridx)
    return None

def checklineofsight(row, col, grid):
    seen = set()

    seen.add(scanrow(grid,col-1,-1,row,step=-1))
    seen.add(scanrow(grid,col+1,len(grid[row])+1,row))
    seen.add(scancol(grid,row-1,-1,col,step=-1))
    seen.add(scancol(grid,row+1,len(grid)+1,col))
    seen.add(scandiagonal(grid,row,col,1,1))
    seen.add(scandiagonal(grid,row,col,-1,1))
    seen.add(scandiagonal(grid,row,col,1,-1))
    seen.add(scandiagonal(grid,row,col,-1,-1))
    
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
    stablegrid = repeatuntilstable(startgrid, verbose=True)
    print(f'Stable grid found, occupied seats: {countoccupied(stablegrid)}')

if __name__ == '__main__':
    sys.exit(main())