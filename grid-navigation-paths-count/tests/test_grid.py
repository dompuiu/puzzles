from unittest import TestCase
from grid_path.grid import Grid

class TestGrid(TestCase):
    def test_init_with_strings(self):
        self.assertRaises(TypeError, Grid, "heigh", "width")

    def test_init_with_negative_dimensions(self):
        self.assertRaises(ValueError, Grid, -1, -1)

    def test_get_permutations_with_zero_width(self):
        self.assertEqual(Grid(0, 1).get_directions_list(), set(['U']))

    def test_get_permutations_with_zero_height(self):
        self.assertEqual(Grid(1, 0).get_directions_list(), set(['R']))

    def test_get_permutations_with_unit_grid(self):
        self.assertEqual(Grid(1, 1).get_directions_list(), set(['RU', 'UR']))

    def test_get_permutations_with_2w_1h(self):
        self.assertEqual(Grid(2, 1).get_directions_list(), set(['RUR', 'RRU', 'URR']))

    def test_get_permutations_with_2w_2h(self):
        self.assertEqual(Grid(2, 2).get_directions_list(), set(['RRUU', 'RURU', 'RUUR', 'URUR', 'URRU', 'UURR']))

    def test_check_length_concordance(self):
        g = Grid(5,5)
        self.assertEqual(len(g.get_directions_list()), g.paths_count())