import re
from sys import stdin

def read_grid_dimensions():
    while True:
        print("Enter grid dimmension (NxM)")
        grid_size_str = stdin.readline()

        match = re.match("^(\d+)[x,X](\d+)$", grid_size_str)
        if match:
            w = int(match.group(1))
            h = int(match.group(2))

            if w > 1 and h > 1:
                break
            else:
                print("The grid dimensions must be larger than 1x1")
    return w, h