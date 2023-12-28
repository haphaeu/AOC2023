data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

data = open("day14.txt").read()

lines = data.strip().splitlines()


def show(lines):
    print("\n".join(lines))


def transpose(lines):
    return ["".join(row) for row in zip(*lines)]


def weight_north_pillar(rolled):
    weight = 0
    for r, row in enumerate(rolled[::-1]):
        weight += row.count("O") * (r + 1)
    return weight


def roll_north(rolled):
    for r in range(1, len(rolled)):
        for c in range(len(rolled[0])):
            if rolled[r][c] == "O" and rolled[r - 1][c] == ".":
                k = 0
                while r - k - 1 >= 0 and rolled[r - k - 1][c] == ".":
                    k += 1
                rolled[r - k] = rolled[r - k][:c] + "O" + rolled[r - k][c + 1 :]
                rolled[r] = rolled[r][:c] + "." + rolled[r][c + 1 :]


def roll_south(rolled):
    """Same as roll_north with rows reversed."""
    tmp = rolled[::-1]
    roll_north(tmp)
    rolled[:] = tmp[::-1]


def roll_west(rolled):
    """Same as roll_north with rows transposed."""
    tmp = transpose(rolled)
    roll_north(tmp)
    rolled[:] = transpose(tmp)


def roll_east(rolled):
    """Same as roll_south with rows transposed."""
    tmp = transpose(rolled)
    roll_south(tmp)
    rolled[:] = transpose(tmp)


def do_one_cycle(rolled):
    roll_north(rolled)
    roll_west(rolled)
    roll_south(rolled)
    roll_east(rolled)


# Part 1
rolled = lines[:]
roll_north(rolled)
weight = weight_north_pillar(rolled)
print("Part 1:", weight)

# Part 2
rolled = lines[:]

possibilities = []
possibilities.append(rolled.__repr__())
weights = [0]


cycle = 0
while True:
    cycle += 1
    do_one_cycle(rolled)
    if rolled.__repr__() in possibilities:
        first = possibilities.index(rolled.__repr__())
        period = cycle - first
        print(f"Cycle pattern found! Start at {first} with {period=} at cycle {cycle}.")
        break

    weight = weight_north_pillar(rolled)
    possibilities.append(rolled.__repr__())
    weights.append(weight)

for cycle in range(first, first + period + 1):
    if (1_000_000_000 - cycle) % period == 0:
        print(f"Part 2: {weights[cycle]}")
        break
