import sys
import unittest

class Day5Tests(unittest.TestCase):
    def test_decoderow(self):
        row, _ = decode('FBFBBFFRLR')
        self.assertEquals(row, 44)

    def test_getrowcode(self):
        rowcode = 'FBFBBFFRLR'[0:7]
        self.assertEqual(7, len(rowcode))
        rowcode = rowcode.replace('F', '0').replace('B', '1')
        self.assertEqual('0101100', rowcode)

def decode(seatcode):
    rowcode = seatcode[0:7]
    rowcode = rowcode.replace('F', '0').replace('B', '1')    
    return int(rowcode, 2), None

def main():
    print('Day 5')

if __name__ == '__main__':
    sys.exit(main())