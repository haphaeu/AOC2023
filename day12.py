import re
import itertools

"""
. operating springs
# damaged springs
? unkown status
groups: the size of each contiguous group of damaged springs
"""

data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

with open("day12.txt") as f:
    data = f.read()


# deprecated - solution for part2 is more efficient and applies for part 1
# all possible combinations of '.' and '#' for a given length
def gen_all_combinations(length=8):
    for i in range(0, 2**length):
        yield bin(i)[2:].zfill(length).replace("0", ".").replace("1", "#")


# all possible combinations of '.' and '#' for a given mask
#  ..##??..##??.##
#  0011??0011??011 ==> only 4off `?`
def gen_all_combinations_mask(mask):
    # ..#??.##?#  => 001??011?1
    length = mask.count("?")
    for i in range(0, 2**length):
        fill = bin(i)[2:].zfill(length).replace("0", ".").replace("1", "#")
        combination = ""
        for c in mask:
            if c == "?":
                combination += fill[0]
                fill = fill[1:]
            else:
                combination += c
        yield combination


def gen_regular_expression(springs, groups):
    # Matches the groups
    expression = r"^"
    for i, g in enumerate(groups):
        expression += r"[\.\?]%c#{%d}" % ("*" if i == 0 else "+", g)
    expression += r"[\.\?]*$"

    # Matches the known springs:
    #   operating springs `.` are replaced with `\.` to match a literal `.`
    #   unkown springs `?` are replaced with `.` to match any character
    expression2 = springs.replace(".", r"\.").replace("?", ".")
    return re.compile(expression), re.compile(expression2)


def count_combinations(springs, groups):
    e1, e2 = gen_regular_expression(springs, groups)
    combinations = []
    for combination in gen_all_combinations_mask(springs):
        if e1.match(combination) and e2.match(combination):
            combinations.append(combination)
    return combinations


def part1(springs_groups):
    all_count = 0
    for i, (springs, groups) in enumerate(springs_groups):
        combinations = count_combinations(springs, groups)
        count = len(combinations)
        all_count += count
        print(f"{i=}: {count=:4d}, {all_count=}", end="\r")
    print(f"\n{all_count=}")


def part2(springs_groups):
    all_count = 0
    for i, (springs, groups) in enumerate(springs_groups):
        print(f"""{i=}: {springs=}, {groups=}, {all_count=:4d}""", end=" ")
        combinations1 = count_combinations(springs, groups)
        combinations2 = count_combinations("?" + springs, groups)
        combinations3 = count_combinations(springs + "?", groups)
        print(
            f"-> found {len(combinations1)}, {len(combinations2)}, {len(combinations3)} combs",
            end=" ",
        )
        e1, e2 = gen_regular_expression("?".join([springs] * 5), groups * 5)
        combinations_all = []
        for comb in itertools.product(
            combinations1, combinations2, combinations2, combinations2, combinations2
        ):
            comb = "".join(comb)
            if e1.match(comb) and e2.match(comb):
                combinations_all.append(comb)
        for comb in itertools.product(
            combinations3, combinations3, combinations3, combinations3, combinations1
        ):
            comb = "".join(comb)
            if e1.match(comb) and e2.match(comb):
                combinations_all.append(comb)
        combinations_all = sorted(list(set(combinations_all)))
        all_count += len(combinations_all)
        print(f"-> {len(combinations_all)}, {all_count=}")
    print(f"\n{all_count=}")


lines = data.splitlines()

springs_groups = []
for i, line in enumerate(lines):
    springs, groups = line.split(" ")
    groups = tuple(map(int, groups.split(",")))
    springs_groups.append((springs, groups))

# part1(springs_groups)
# Output: 7541

part2(springs_groups)
# this is not promissing, it would take forever to run
# giving up on this approach... see `day12_cheat.py`
