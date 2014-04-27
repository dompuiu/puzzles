from unittest import TestCase
from grid_path.string_permutations import Permutations


class TestPermutations(TestCase):
    def test_get_permutations_with_empty_string(self):
        self.assertEqual(Permutations('').get_permutations(), set(['']))

    def test_get_permutations_with_one_letter_word(self):
        self.assertEqual(Permutations('A').get_permutations(), set(['A']))

    def test_get_permutations_with_two_letters_word(self):
        self.assertEqual(Permutations('AB').get_permutations(), set(['AB', 'BA']))

    def test_get_permutations_with_three_letters_word(self):
         self.assertEqual(Permutations('ABC').get_permutations(), set(['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']))

    def test_get_permutations_with_same_letter_word(self):
         self.assertEqual(Permutations('AA').get_permutations(), set(['AA']))