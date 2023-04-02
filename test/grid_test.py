import unittest
import context

from arya import Grid

class TestGrid(unittest.TestCase):

    def test_initialization(self):
        grid = Grid(2, 3)
        self.assertEqual(grid.nrows, 2)
        self.assertEqual(grid.ncols, 3)
        self.assertEqual(grid.grid, [[None, None, None], [None, None, None]])

    def test_get_set_item(self):
        grid = Grid(2, 3)

        grid[0, 0] = 'A'
        grid[1, 2] = 'B'

        self.assertEqual(grid[0, 0], 'A')
        self.assertEqual(grid[1, 2], 'B')

    def test_add_item(self):
        grid = Grid()

        grid.add_item(0, 0, 'A')
        grid.add_item(1, 1, 'B')
        grid.add_item(2, 2, 'C')

        self.assertEqual(grid.nrows, 3)
        self.assertEqual(grid.ncols, 3)
        self.assertEqual(grid[0, 0], 'A')
        self.assertEqual(grid[1, 1], 'B')
        self.assertEqual(grid[2, 2], 'C')

    def test_iter(self):
        grid = Grid(3, 3)

        grid[0, 0] = 'A'
        grid[1, 1] = 'B'
        grid[2, 2] = 'C'

        result = [(row, col, element) for row, col, element in grid]
        expected = [
            (0, 0, 'A'),
            (1, 1, 'B'),
            (2, 2, 'C'),
        ]
        self.assertEqual(result, expected)

    def test_strict_mode(self):
        grid = Grid(2, 3, strict=True)

        grid[0, 0] = 'A'

        with self.assertRaises(ValueError):
            grid[0, 0] = 'B'

if __name__ == '__main__':
    unittest.main()
