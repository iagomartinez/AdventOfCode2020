import sys
import unittest
from parameterized import parameterized

class Day5Tests(unittest.TestCase):
    @parameterized.expand([
        ('FBFBBFFRLR', 44, 5, 357),
        ('BFFFBBFRRR', 70, 7, 567),
        ('FFFBBBFRRR', 14, 7, 119),
        ('BBFFBBFRLL', 102, 4, 820)
    ])
    def test_decodeseat(self, code, exprow, expcol, expseatid):
        row, col, seatid = decode(code)
        self.assertEqual((exprow,expcol,expseatid), (row,col, seatid))

    def test_decoderow(self):
        rowcode = 'FBFBBFFRLR'[0:7]
        self.assertEqual(7, len(rowcode))
        rowcode = rowcode.replace('F', '0').replace('B', '1')
        self.assertEqual('0101100', rowcode)

    def test_decodecol(self):
        colcode = 'FBFBBFFRLR'[7:11]
        self.assertEqual(3, len(colcode))
        colcode = colcode.replace('R','1').replace('L','0')
        self.assertEqual('101', colcode)

    def test_max(self):
        seatids = calculate('../_data/day5.txt')
        self.assertEqual(980, max(seatids))

def decode(seatcode, verbose=False):
    rowcode = seatcode[0:7]
    rowcode = rowcode.replace('F', '0').replace('B', '1')
    rowcode = int(rowcode, 2)
    colcode = seatcode[7:11]
    colcode = colcode.replace('R','1').replace('L','0')
    colcode = int(colcode, 2)

    seatid = (rowcode * 8) + colcode
    if verbose:
        print(f'{seatcode}-># r:{rowcode}, c:{colcode}, id:{seatid}')

    return rowcode, colcode, seatid

def calculate(datafile, verbose=False):
    seatids = []
    with open('../_data/day5.txt', 'r', newline='', encoding='utf-8') as f:
        for line in f:
            code = line.rstrip()
            _, _,id = decode(code, verbose)
            seatids.append(id)
    return seatids

def main():    
    seatids = calculate('../_data/day5.txt', True)
    print(max(seatids))

    seatids.sort()
    front = seatids[0:len(seatids)-1]
    back = seatids[1:len(seatids)]
    for seat1, seat2 in zip(front, back):
        if seat2 != seat1 + 1:
            print(f'missing seat is {seat1 + 1}')
            break

if __name__ == '__main__':
    sys.exit(main())