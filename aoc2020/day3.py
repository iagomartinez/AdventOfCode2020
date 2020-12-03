import sys
import unittest

class ValidationTests(unittest.TestCase):
    def test_sample(self):
        tree_count = toboggan('../_data/day3_sample.txt')
        self.assertEquals(tree_count, 7)

def toboggan(mapfile):
    with open(mapfile, 'r',newline='', encoding='utf-8') as f:
        tree_count = None
    return tree_count

def main():
    toboggan('../_data/day3.txt')
    
if __name__ == '__main__':
    unittest.main()
    #sys.exit(main())