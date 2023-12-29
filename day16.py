import sys

data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".strip()

data = open("day16.txt").read().strip()

GRID = data.splitlines()
YLIM = len(GRID)
XLIM = len(GRID[0])

ENERGISED = [[0] * XLIM for _ in range(YLIM)]

MEMO_CACHE = set()


def ray_trace(x=0, y=0, dx=1, dy=0):
    """Trace a ray starting at (x, y) in direction (dx, dy) in a grid.

    Python can't handle deep recursion, so each step return the next point
    and direction - need to handle that for splitters, two rays are returned.

    `x` is horizontal, from left to right.     o--->
    `y` is vertical, from top to bottom.       |   x
                                               v  y
    The ray behaves as follows:

        `.` is empty space, the ray continues in the same direction

        `|` is a vertical splitter, a horizontally travelling ray is split
            in two, one travelling up and one travelling down.
            A vertically travelling ray is not affected.

        `-` is a horizontal splitter, a vertically travelling ray is split
            in two, one travelling left and one travelling right.
            A horizontally travelling ray is not affected.

        `/` is a mirror, the ray is reflected 90 deg. If coming from the left,
            it continues up; if coming from the right, it continues down; if
            coming from above, it continues left; if coming from below, it
            continues right.

        `\` is a mirror, the ray is reflected 90 deg. If coming from the left,
            it continues down; if coming from the right, it continues up; if
            coming from above, it continues right; if coming from below, it
            continues left.
    """

    assert (
        dx + dy in (1, -1) and dx * dy == 0
    ), "Direction must be horizontal or vertical"

    # Exit if out of the grid's bounds
    if x < 0 or x >= XLIM or y < 0 or y >= YLIM:
        # print("Ray exited at ({}, {})".format(x, y))
        return

    # memo cache - if ray comes back to same location, with same speed, it's
    # a loop, and we can stop
    if (x, y, dx, dy) in MEMO_CACHE:
        # print("Ray looped at ({}, {})".format(x, y))
        return
    MEMO_CACHE.add((x, y, dx, dy))

    ENERGISED[y][x] = 1
    action = GRID[y][x]

    if action in "./\\":
        if action == "/":
            dx, dy = -dy, -dx
        elif action == "\\":
            dx, dy = dy, dx
        return [(x + dx, y + dy, dx, dy)]

    elif action in "|-":
        if (action == "|" and dx == 0) or (action == "-" and dy == 0):
            return [(x + dx, y + dy, dx, dy)]
        else:
            if action == "|":
                dx, dy = 0, 1
            elif action == "-":
                dx, dy = 1, 0
            return [(x + dx, y + dy, dx, dy), (x - dx, y - dy, -dx, -dy)]
    else:
        raise ValueError(f"Invalid action {action}")


def energise_grid(x, y, dx, dy):
    """Return the energy of the grid after the ray starting at x, y
    moving with speed dx, dy has been traced.
    """

    global ENERGISED, MEMO_CACHE
    ENERGISED = [[0] * XLIM for _ in range(YLIM)]
    MEMO_CACHE = set()

    ray_stack = set()
    while True:
        next_rays = ray_trace(x, y, dx, dy)
        if next_rays is None:
            if len(ray_stack) == 0:
                break
            else:
                x, y, dx, dy = ray_stack.pop()
                continue
        if len(next_rays) == 2:
            ray_stack.add(next_rays[1])
        x, y, dx, dy = next_rays[0]

    return sum(sum(row) for row in ENERGISED)


def part1():
    x, y, dx, dy = 0, 0, 1, 0
    print("Part 1:", energise_grid(x, y, dx, dy))


def part2():
    max_energy = 0
    for x in range(XLIM):
        max_energy = max(
            max_energy, energise_grid(x, 0, 0, 1), energise_grid(x, YLIM - 1, 0, -1)
        )
    for y in range(YLIM):
        max_energy = max(
            max_energy, energise_grid(0, y, 1, 0), energise_grid(XLIM - 1, y, -1, 0)
        )
    print("Part 2:", max_energy)


part1()
part2()
