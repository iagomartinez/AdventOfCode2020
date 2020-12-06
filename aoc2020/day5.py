import sys
import unittest

class Day5Tests(unittest.TestCase):
    def test_decoderow(self):
        row, _ = decode('FBFBBFFRLR')
        self.assertEquals(row, 44)

def decode(row):
    return None, None

def main():
    print('Day 5')

if __name__ == '__main__':
    sys.exit(main())