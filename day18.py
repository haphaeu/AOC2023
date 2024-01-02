"""
This works nicely for Part 1, with visual lake maps saved to text files.
But it explodes the memonry brutally for Part 2... giving up for now...
"""

import numpy as np
import time

SAVETEXTMAPS = True
VERBOSE = True


def savetxt(filename, arr):
    """Save array to text file, with `#` for 1 and `.` for 0, no spaces."""
    np.savetxt(filename, arr, fmt="%d")
    with open(filename, "r") as f:
        cont = f.read()
    with open(filename, "w") as f:
        f.write(cont.replace("1", "#").replace("0", ".").replace(" ", ""))


def savetxt2(filename, arr):
    """Save array to text file, with `.`, `-`, `|`, `F`, `J`, `L`, `7`
    for 0, 1, 2, 3, 4, 5, 6, respectively, no spaces.
    """
    np.savetxt(filename, arr, fmt="%d")
    with open(filename, "r") as f:
        cont = f.read()
    with open(filename, "w") as f:
        for fr, to in zip("0123456", ".-|FJL7"):
            cont = cont.replace(fr, to)
        f.write(cont.replace(" ", ""))


def timer(func):
    """Decorator to time a function."""

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f}s")
        return res

    return wrapper


@timer
def do_dig(dig_plan):
    # %% Calc footprint of lake
    xmax, xmin, ymax, ymin = 0, 0, 0, 0
    x, y = 0, 0
    for dig in dig_plan:
        dir, dist, color = dig
        if dir == "R":
            x += dist
        elif dir == "L":
            x -= dist
        elif dir == "U":
            y -= dist
        elif dir == "D":
            y += dist
        xmax = max(xmax, x)
        xmin = min(xmin, x)
        ymax = max(ymax, y)
        ymin = min(ymin, y)
    print(f"{xmin=}, {xmax=}, {ymin=}, {ymax=}")
    xrange = xmax - xmin + 1
    yrange = ymax - ymin + 1

    # %% Dig borders

    M, N = xrange, yrange
    lake = np.zeros((N, M), dtype=int)
    x, y = -xmin, -ymin
    for dig in dig_plan:
        dir, dist, color = dig
        if dir == "R":
            lake[y, x : x + dist + 1] = 1
            x += dist
        elif dir == "L":
            lake[y, x - dist : x] = 1
            x -= dist
        if dir == "U":
            lake[y - dist : y, x] = 1
            y -= dist
        elif dir == "D":
            lake[y : y + dist + 1, x] = 1
            y += dist

    if SAVETEXTMAPS:
        savetxt("day18_lake_border.txt", lake)
    print(f"total perimeter: {lake.sum()}")

    # %% Convert array to text with characters for the borders and corners,
    # using `-` and `|` for horizontal and vertical borders, respectively,
    # and `F`, `J`, `L`, `7` for the corners, as in the following example.
    # But first, use numbers only, `-` is 1, `|` is 2, `F` is 3, `J` is 4,
    # `L` is 5, `7` is 6.
    #
    #      F---7     31116
    #      |   |     2   2
    #      L---J     51114
    #

    lake2 = np.zeros_like(lake)
    for y in range(N):
        for x in range(M):
            if lake[y, x] == 0:
                continue
            if (x == 0 or lake[y, x - 1] == 0) and (x == M - 1 or lake[y, x + 1] == 0):
                lake2[y, x] = 2
            elif (y == 0 or lake[y - 1, x] == 0) and (
                y == N - 1 or lake[y + 1, x] == 0
            ):
                lake2[y, x] = 1
            elif (y == 0 or lake[y - 1, x] == 0) and (x == 0 or lake[y, x - 1] == 0):
                lake2[y, x] = 3
            elif (y == N - 1 or lake[y + 1, x] == 0) and (
                x == M - 1 or lake[y, x + 1] == 0
            ):
                lake2[y, x] = 4
            elif (y == N - 1 or lake[y + 1, x] == 0) and (
                x == 0 or lake[y, x - 1] == 0
            ):
                lake2[y, x] = 5
            elif (y == 0 or lake[y - 1, x] == 0) and (
                x == M - 1 or lake[y, x + 1] == 0
            ):
                lake2[y, x] = 6

    if SAVETEXTMAPS:
        savetxt2("day18_lake_symbols.txt", lake2)

    # %% Dig interior

    lake3 = lake.copy()

    # Mark inside points
    # Scan the lake from top to bottom, then left to right
    for y in range(N - 1):
        inside = False
        for x in range(M - 1):
            if lake2[y, x] == 0:
                lake3[y, x] = 1 if inside else 0
            elif lake2[y, x] == 1:  # horizontal border:do nothing
                continue
            elif lake2[y, x] == 2:  # cross vertical border
                inside = not inside
            elif lake2[y, x] == 3:  # F-7 no border or F-J: border
                j = x + 1
                while lake2[y, j] == 1:  # -
                    j += 1
                if lake2[y, j] == 4:  # J
                    inside = not inside
                else:
                    assert lake2[y, j] == 6  # 7
            elif lake2[y, x] == 5:  # L--7: border or L-J: no border
                j = x + 1
                while lake2[y, j] == 1:  # -
                    j += 1
                if lake2[y, j] == 6:  # 7
                    inside = not inside
                else:
                    assert lake2[y, j] == 4  # J
            else:
                assert lake2[y, x] in (4, 6)  # J or 7

    if SAVETEXTMAPS:
        savetxt("day18_lake_interior.txt", lake3)
    print(f"total area: {lake3.sum()}")


# %% DATA
data = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""".strip()

data = open("day18.txt").read().strip()

lines = data.splitlines()

# %% Part 1
print("Part 1")

SAVETEXTMAPS = True
VERBOSE = True

dig_plan = [i.split() for i in lines]
dig_plan = [(i, int(j), k) for i, j, k in dig_plan]
do_dig(dig_plan)

# %% Part 2
print("Part 2")

SAVETEXTMAPS = False

dig_plan2 = []
for _, _, code in dig_plan:
    # code has format: `(#6248a0)
    dist = eval("0x" + code[2:7])
    d = int(code[7])
    assert 0 <= d <= 3
    dir = "R" if d == 0 else ("D" if d == 1 else ("L" if d == 2 else "U"))
    dig_plan2.append((dir, dist, code))

do_dig(dig_plan2)
# %%
