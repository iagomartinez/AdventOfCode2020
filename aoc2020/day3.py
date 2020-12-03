import sys
import unittest

class ValidationTests(unittest.TestCase):
    def test_sample(self):
        tree_count = toboggan('../_data/day3_sample.txt')
        self.assertEquals(tree_count, 7)

    def test_tree_hit(self):
        self.assertEquals(tree_hit('..##.......', 0), 0)
        self.assertEquals(tree_hit('..##.......', 2), 1)

    def test_next_pos(self):
        self.assertEquals(next_pos(pos_x=0, step_size=3, row='..##.......'), 3)

    def test_next_pos_on_edge(self):
        self.assertEquals(next_pos(pos_x=10, step_size=3, row='..##.......'), 2)

def next_pos(pos_x, step_size, row):
    return (pos_x + step_size) % len(row)

def tree_hit(row, pos_x):
    return row[pos_x] == '#'

def toboggan(mapfile):
    tree_count = 0
    pos_x = 0
    with open(mapfile, 'r',newline='', encoding='utf-8') as f:
        for row in f:
            stripped_line = row.rstrip()
            tree_count += tree_hit(stripped_line, pos_x)
            pos_x = next_pos(pos_x, step_size=3, row=stripped_line)
    return tree_count

def main():
    print(toboggan('../_data/day3.txt'))
    
if __name__ == '__main__':
    #unittest.main()
    sys.exit(main())