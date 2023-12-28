data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
\t
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

data = open("day13.txt").read()

lines = data.strip().splitlines()

# extract patterns
puzzles = []
tmp = []
lines.append("\t")
for line in lines:
    if line.strip() == "":
        puzzles.append(tmp)
        tmp = []
    else:
        tmp.append(line)


def transpose(puzzle):
    """#..    ###
    ##. => .##
    ###    ..#
    """
    return ["".join(c) for c in zip(*puzzle)]


def find_reflections_pt1(puzzle):
    """Strategy: iterate over rows, and try to find to identical rows.
    Then, go over to the previous and next rows and check if they are
    also identical. If this pattern repeats until one side reaches the
    end of the grid, we have found a reflection.
    Then, do the same for the columns.
    """
    # Iterate over rows
    for i in range(1, len(puzzle)):
        # Check 2 sequential rows for equality
        if puzzle[i - 1] == puzzle[i]:
            reflection = True
            # found 2 matching rows, now check if this pattern repeats
            # going simultaneously to the next and previous,
            # ie, (i+1, i-2), (i+2, i-3) ==> (i+j+1, i-j-2)
            # for j from zero until the end of the grid
            for j in range(min(len(puzzle) - i - 1, i - 1)):
                if puzzle[i + j + 1] != puzzle[i - j - 2]:
                    # pattern does not repeat...
                    reflection = False
                    break
            else:
                # pattern repeats, we have found a reflection
                # store how many lines before the reflection line
                return i

    return 0


def find_reflections_pt2(puzzle):
    """Mostly copy of part 1. But when pattern is broken, check
    if the difference is one, and exactly one character.
    """
    # Iterate over rows
    for i in range(1, len(puzzle)):
        swaps = 0
        # Check 2 sequential rows for equality
        if puzzle[i - 1] != puzzle[i]:
            # check if diff is only 1 character

            diffs = []
            for c, (a, b) in enumerate(zip(puzzle[i - 1], puzzle[i])):
                if a != b:
                    diffs.append(c)
            if len(diffs) == 1:
                swaps += 1
                if swaps > 1:
                    raise Exception("more than one swap 1")

                for j in range(min(len(puzzle) - i - 1, i - 1)):
                    if puzzle[i + j + 1] != puzzle[i - j - 2]:
                        # pattern breaks
                        break
                else:
                    # it must swap...
                    if swaps != 1:
                        return -1
                    # pattern repeats, we have found a reflection
                    # store how many lines before the reflection line
                    return i

        else:  # if puzzle[i - 1] == puzzle[i]:
            reflection = True
            # found 2 matching rows, now check if this pattern repeats
            # going simultaneously to the next and previous,
            # ie, (i+1, i-2), (i+2, i-3) ==> (i+j+1, i-j-2)
            # for j from zero until the end of the grid

            for j in range(min(len(puzzle) - i - 1, i - 1)):
                if puzzle[i + j + 1] != puzzle[i - j - 2]:
                    # pattern breaks, check if the difference is
                    # only 1 character:
                    diffs = []
                    for c, (a, b) in enumerate(
                        zip(puzzle[i + j + 1], puzzle[i - j - 2])
                    ):
                        if a != b:
                            diffs.append(c)
                    if len(diffs) > 1:
                        reflection = False
                        break
                    else:
                        swaps += 1
                        if swaps == 1:
                            puzzle[i - j - 2] = puzzle[i + j + 1]
                        else:
                            continue

            else:
                # it must swap...
                if swaps != 1:
                    return -1
                # pattern repeats, we have found a reflection
                # store how many lines before the reflection line
                return i

    return 0


def part1():
    all_sum = 0
    for puzzle in puzzles:
        all_sum += 100 * find_reflections_pt1(puzzle)
        all_sum += find_reflections_pt1(transpose(puzzle))
    print(all_sum)


def show(puz):
    for p in puz:
        print("    ", p)


def part2():
    all_sum = 0
    for puzzle in puzzles:
        print("New Puzzle")
        show(puzzle)

        # print("  vertical/columns")
        # puz = transpose(puzzle)
        # refls = find_reflections_pt2(puz)
        # is_smudge_fixed = True
        # if refls == -1:
        #     print("    no swap... trying horizontal first")
        #     is_smudge_fixed = False
        # elif refls > 0:
        #     print(f"    Vertical reflection at column {refls}")
        #     puzzle = transpose(puz)
        #     show(puzzle)
        #     all_sum += refls
        # else:
        #     print("    no reflections")

        print("  horizontal/rows")
        # if is_smudge_fixed:
        #     refls = find_reflections_pt1(puzzle)
        # else:
        #     refls = find_reflections_pt2(puzzle)
        #     assert not refls == -1, "smudge should be fixed here"
        refls = find_reflections_pt2(puzzle)
        print(f"    Horizontal reflection at column {refls}")
        show(puzzle)
        if refls > -1:
            all_sum += 100 * refls

        # if not is_smudge_fixed:
        #     print("  re-trying vertical/columns")
        #     puz = transpose(puzzle)
        #     refls = find_reflections_pt1(puz)
        #     print(f"    Vertical reflection at column {refls}")
        #     puzzle = transpose(puz)
        #     show(puzzle)
        #     all_sum += refls

    print(all_sum)


part2()
