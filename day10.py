data = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

with open("day10.txt") as f:
    data = f.read()

lines = data.splitlines()


def find_next(row, col, lines, from_row, from_col):
    """Follows the path and return (row, col) of the next step.
    Previous step is given to avoid the path to "come back".
    
    Possible connections are:
    |:              -:
        [7|F]               x
         x|x           [L-F]-[7-J]
        [J|L]               x

    7:              J:
            x               [7|F]
       [L-F]7x           [L-F]Jx
          [J|L]               x

    L:               F:
       [7|F]         x
        xL[7-J]     xF[7-J]
         x         [J|L]

    """
    c = lines[row][col]
    if c == "|":
        if lines[row - 1][col] in "7|FS" and (row - 1, col) != (from_row, from_col):
            return row - 1, col
        elif lines[row + 1][col] in "J|LS" and (row + 1, col) != (from_row, from_col):
            return row + 1, col
        else:
            return None
    elif c == "-":
        if lines[row][col - 1] in "L-FS" and (row, col - 1) != (from_row, from_col):
            return row, col - 1
        elif lines[row][col + 1] in "7-JS" and (row, col + 1) != (from_row, from_col):
            return row, col + 1
        else:
            return None
    elif c == "7":
        if lines[row][col - 1] in "L-FS" and (row, col - 1) != (from_row, from_col):
            return row, col - 1
        elif lines[row + 1][col] in "J|LS" and (row + 1, col) != (from_row, from_col):
            return row + 1, col
        else:
            return None
    elif c == "J":
        if lines[row - 1][col] in "7|FS" and (row - 1, col) != (from_row, from_col):
            return row - 1, col
        elif lines[row][col - 1] in "L-FS" and (row, col - 1) != (from_row, from_col):
            return row, col - 1
        else:
            return None
    elif c == "L":
        if lines[row][col + 1] in "7-JS" and (row, col + 1) != (from_row, from_col):
            return row, col + 1
        elif lines[row - 1][col] in "7|FS" and (row - 1, col) != (from_row, from_col):
            return row - 1, col
        else:
            return None
    elif c == "F":
        if lines[row][col + 1] in "7-JS" and (row, col + 1) != (from_row, from_col):
            return row, col + 1
        elif lines[row + 1][col] in "J|LS" and (row + 1, col) != (from_row, from_col):
            return row + 1, col
        else:
            return None
    else:
        return None


def find_first(start, lines):
    row, col = start
    if lines[row - 1][col] in "7|F":
        return row - 1, col
    elif lines[row + 1][col] in "J|L":
        return row + 1, col
    elif lines[row][col - 1] in "L-F":
        return row, col - 1
    elif lines[row][col + 1] in "7-J":
        return row, col + 1
    else:
        return None


def find_start(lines):
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "S":
                return row, col

# Part 1
#   1. find starting point, `start`
#   2. choose next point, `first`
#   3. follow the path until back to start
#
# `visited` nodes are only kept to re-write the file without clutter, ie,
# keeping only the main loop.

visited = set()
start = find_start(lines)
visited.add(start)
first = find_first(start, lines)
assert first is not None
row_from, col_from = start
row, col = first
path = "S"
while True:
    print(lines[row][col], end="")
    visited.add((row, col))
    path += lines[row][col]
    next = find_next(row, col, lines, row_from, col_from)
    assert next is not None
    if next == start:
        break
    row_from, col_from = row, col
    row, col = next
print(path)
print(len(path) // 2)
# Output: 6806


# Part 2
# Simple test to see if a point (x,y) is enclosed within a curve:
#  Draw a ray from (x,y) to infinity, and count how many times it crosses the curve;
#  if the count is odd, then (x,y) is inside the enclosed region; otherwise, it's outside.

# First, clean up what is not in the main loop
# Anything that is not part of the main loop is replace by terrain '.':
with open("day10_main_loop.txt", "w") as f:
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if (row, col) in visited:
                f.write(lines[row][col])
            else:
                f.write(".")
        f.write("\n")

with open("day10_main_loop.txt") as f:
    data = f.read()
lines = data.splitlines()

# little cheat, replace S by its real value:
lines[start[0]] = lines[start[0]].replace("S", "J")

# Ray tracing to count border crossings
# sending a "horizontal" ray, ie, won't cross horizontal pipe '-'
with open("day10_nest.txt", "w") as f:
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == ".":
                count_crossings = 0
                for i in range(col, -1, -1):
                    if lines[row][i] in "|LJ":
                        count_crossings += 1
                if count_crossings % 2 == 1:
                    f.write("#")  # inside
                else:
                    f.write(" ")  # outside
            else:
                f.write(c)
        f.write("\n")

with open("day10_nest.txt") as f:
    data = f.read()
data.count("#")
# Output: 449
