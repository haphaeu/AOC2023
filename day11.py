import numpy as np

data="""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

with open('day11.txt') as f:
    data = f.read()

lines = data.splitlines()

# find galaxies
galaxies_coords = []
for row, line in enumerate(lines):
    for col, c in enumerate(line):
        if c == '#':
            galaxies_coords.append((row, col))

# find empty rows and cols
empty_rows = []
for row, line in enumerate(lines):
    if set(line) == {'.'}:
        empty_rows.append(row)
empty_cols= []
for col, line in enumerate([''.join(c) for c in zip(*lines)]):
    if set(line) == {'.'}:
        empty_cols.append(col)

# expand space

# expansion = 2  # part 1
expansion = 1000000 - 1  # part 2
galaxies_coords_expanded = []
for galaxy_coord in galaxies_coords:
    galaxy_row, galaxy_col = galaxy_coord
    expand_rows, expand_cols = 0, 0
    for r in empty_rows:
        if galaxy_row > r:
            expand_rows += expansion
    for c in empty_cols:
        if galaxy_col > c:
            expand_cols += expansion
    galaxies_coords_expanded.append((
        galaxy_row + expand_rows,
        galaxy_col + expand_cols
    ))

# get distances
sum_distances = 0
for i, coord1 in enumerate(galaxies_coords_expanded):
    x1, y1 = coord1
    for j, coord2 in enumerate(galaxies_coords_expanded[i+1:]):
        x2, y2 = coord2
        distance = abs(x2-x1) + abs(y2-y1)
        sum_distances += distance
        
print(sum_distances)

# For part 1 and 2, just change `expansion` above.
# `expansion = 2` for part 1
# `expansion = 1000000 - 1` for part 2
# Part 1 9795148
# Part 2 650672493820
