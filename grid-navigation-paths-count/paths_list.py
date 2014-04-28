from grid_path.grid import Grid
from grid_path.grid_dimensions import read_grid_dimensions

i = 1
w, h = read_grid_dimensions()
g = Grid(w-1, h-1)

print("For a %s x %s grid the possible variants are:" % (w, h))

for solution in g.get_directions_list():
    print ("%.5d. %s" % (i, solution))
    i += 1