import sys
import unittest

class ValidationTests(unittest.TestCase):
    def test_sample(self):
        step_sizes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
        tree_counts = multi_toboggan('../_data/day3_sample.txt', step_sizes)
        print(tree_counts)
        self.assertEquals(product(tree_counts), 336)

    def test_tree_hit(self):
        self.assertEquals(tree_hit('..##.......', 0), 0)
        self.assertEquals(tree_hit('..##.......', 2), 1)

    def test_next_pos(self):
        self.assertEquals(next_pos(pos_x=0, step_size=3, row='..##.......'), 3)

    def test_next_pos_on_edge(self):
        self.assertEquals(next_pos(pos_x=10, step_size=3, row='..##.......'), 2)

def product(tree_counts):
    product = 1
    for c in tree_counts:
        product *= c
    return product

def next_pos(pos_x, step_size, row):
    return (pos_x + step_size) % len(row)

def tree_hit(row, pos_x):
    return row[pos_x] == '#'

def toboggan(mapfile, x_move, y_move):
    tree_count = 0
    pos_x = 0
    with open(mapfile, 'r',newline='', encoding='utf-8') as f:
        line = 0
        for row in f:
            if line % y_move == 0:
                print(f'hit line {line}')
                stripped_line = row.rstrip()
                tree_count += tree_hit(stripped_line, pos_x)
                pos_x = next_pos(pos_x, x_move, row=stripped_line)
            else:
                print(f'skipped line {line}')
            line += 1
    return tree_count

def multi_toboggan(mapfile, step_sizes):
    tree_counts = [toboggan(mapfile, x, y) for x,y in step_sizes]
    return tree_counts

def main():
    step_sizes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    tree_counts = multi_toboggan('../_data/day3.txt', step_sizes)
    print(tree_counts)
    print(product(tree_counts))

if __name__ == '__main__':
    #unittest.main()
    sys.exit(main())