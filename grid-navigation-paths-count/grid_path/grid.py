from grid_path.factorial import factorial
from grid_path.string_permutations import Permutations

class Grid:
    w_direction_string = 'R'
    h_direction_string = 'U'

    def __init__(self, w, h):
        if type(w).__name__ != 'int' or type(h).__name__ != 'int':
            raise TypeError("Grid dimensions must be integers")

        if w < 0 or h < 0:
            raise ValueError("Grid dimensions must not be negative.")

        self.width = w
        self.height = h

    def paths_count(self):
        return factorial(self.width + self.height) / (factorial(self.width) * factorial(self.height))

    def get_directions_list(self):
        return Permutations(self.direction_initial_path()).get_permutations()

    def direction_initial_path(self):
        return self.__class__.w_direction_string * self.width + self.__class__.h_direction_string * self.height