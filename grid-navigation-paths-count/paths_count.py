from grid_path.grid import Grid
from grid_path.grid_dimensions import read_grid_dimensions

w, h = read_grid_dimensions()
g = Grid(w-1, h-1)

print("The number of different paths in a %sx%s grid is equal to %s." % (w, h, g.paths_count()))
