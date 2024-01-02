"""

 IT FUCKING WORKS !!!

 Can't believe (a) I came up with this algo on my own, and that
 (b) it works. There has to be an easier way to implement this...

See day18.xlsx for a visual of the algorithm...
 
"""
import time


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
    # init previous moves
    if dig_plan[0][0] in "UD":
        prev_left = dig_plan[-1][0] == "L"
        prev_dist = dig_plan[-1][1]
        prev_up = dig_plan[-2][0] == "U"
    else:  # 'R' or 'L'
        prev_left = dig_plan[-2][0] == "L"
        prev_dist = dig_plan[-2][1]
        prev_up = dig_plan[-1][0] == "U"

    # walk through the path adding/subtracting area
    x = 0  # it doesn't matter where we start
    area = 0
    for i, (d, dist, code) in enumerate(dig_plan):
        if d == "R":
            x += dist
        elif d == "L":
            x -= dist
        elif d == "D":
            if prev_up:
                if prev_left:  # DUL
                    area += x * (dist + 1) + prev_dist - 1
                else:  # DUR
                    area += x * (dist + 1)
            else:
                if prev_left:  # DDL
                    area += x * dist
                else:  # DDR
                    area += x * dist + prev_dist
        elif d == "U":
            if prev_up:
                if prev_left:  # UUL
                    area += -(x - 1) * dist + prev_dist
                else:  # UUR
                    area += -(x - 1) * dist
            else:
                if prev_left:  # UDL
                    area += -(x - 1) * (dist + 1)
                else:  # UDR
                    area += -(x - 1) * (dist + 1) + prev_dist - 1

        # update previous moves
        if d in "UD":
            prev_up = d == "U"
        else:  # LR
            prev_left = d == "L"
            prev_dist = dist

    print(f"{area=}")


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
print("Part 1:")
dig_plan = [i.split() for i in lines]
dig_plan = [(i, int(j), k) for i, j, k in dig_plan]
do_dig(dig_plan)

# %% Part 2
print("Part 2:")

dig_plan2 = []
for _, _, code in dig_plan:
    # code has format: `(#6248a0)
    dist = eval("0x" + code[2:7])
    d = int(code[7])
    assert 0 <= d <= 3
    dir = "R" if d == 0 else ("D" if d == 1 else ("L" if d == 2 else "U"))
    dig_plan2.append((dir, dist, code))

do_dig(dig_plan2)
