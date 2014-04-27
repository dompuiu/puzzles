from sys import stdin
from grid_path.grid import Grid
import re

while True:
    print("Enter grid dimmension (NxM)")
    grid_size_str = stdin.readline()

    match = re.match("^(\d+)[x,X](\d+)$", grid_size_str)
    if match:
        w = int(match.group(1))
        h = int(match.group(2))

        if w > 0 and h > 0:
            break

g = Grid(w, h)

print("Here is the list of possible steps:")

i = 1
for solution in g.get_directions_list():
    print ("%.5d. %s" % (i, solution))
    i += 1