import re


# data = """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen""".split(
#     "\n"
# )
# # Answer: 281


with open("day01.txt") as f:
    data = f.readlines()

ds = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
ss = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def get_first(line):
    idx_min = 99
    value = -1
    for d in ds:
        idx = line.find(d)
        if idx != -1 and idx < idx_min:
            idx_min = idx
            value = d
    for d in ss:
        idx = line.find(d)
        if idx != -1 and idx < idx_min:
            idx_min = idx
            value = ds[ss.index(d)]
    return int(value)


def get_last(line):
    idx_max = -99
    value = -1
    for d in ds:
        idx = line.rfind(d)
        if idx != -1 and idx > idx_max:
            idx_max = idx
            value = d
    for d in ss:
        idx = line.rfind(d)
        if idx != -1 and idx > idx_max:
            idx_max = idx
            value = ds[ss.index(d)]
    return int(value)


code = 0

for line in data:
    first = get_first(line)
    last = get_last(line)
    # print(line.strip(), first, last)
    code += 10 * first + last

print(code)

# Output: 54431.
