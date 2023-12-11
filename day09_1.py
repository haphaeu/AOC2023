import numpy as np

data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

with open("day09.txt", "r") as f:
    data = f.read()

lines = data.splitlines()
report = [list(map(int, line.split())) for line in lines]


def extrapolate(readings):
    seq = [readings[:]]
    while not np.all((y := np.diff(seq[-1])) == 0):
        seq.append(y)
    return sum([s[-1] for s in seq])


print(sum([extrapolate(readings) for readings in report]))
