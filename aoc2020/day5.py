import sys
import unittest

class Day5Tests(unittest.TestCase):
    def test_decodeseat(self):
        row, col = decode('FBFBBFFRLR')
        self.assertEquals((44,5), (row,col))

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

def decode(seatcode):
    rowcode = seatcode[0:7]
    rowcode = rowcode.replace('F', '0').replace('B', '1')
    colcode = seatcode[7:11]
    colcode = colcode.replace('R','1').replace('L','0')
    return int(rowcode, 2), int(colcode, 2)

def main():
    print('Day 5')

if __name__ == '__main__':
    sys.exit(main())