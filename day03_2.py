import re

# schematic = """
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# """.strip()


with open("day03.txt") as f:
    schematic = f.read()


def is_digit(d):
    try:
        int(d)
        return d
    except ValueError:
        return False


def parse_line(ln, pos):
    numbers = []
    # check after `pos`
    j = 0
    digits = ""
    while digit := is_digit(ln[pos + 1 + j]):
        digits += digit
        j += 1
    if digits:
        numbers.append(digits)
    # check before `pos`
    j = 0
    digits = ""
    while digit := is_digit(ln[pos - 1 - j]):
        digits += digit
        j += 1
    if digits:
        numbers.append(digits[::-1])  # digits are reversed

    return numbers


# find all numbers
pattern_numbers = re.compile(r"\d+")

lines = schematic.splitlines(keepends=True)
sum_gear_ratios = 0
schematic_parts = []
for i, line in enumerate(lines):
    if "*" not in line:
        continue

    print(f"\n{i=}")
    print("".join(lines[max(i - 1, 0) : i + 2]))

    pos = -1
    while (pos := line.find("*", pos + 1)) != -1:
        numbers = []

        # check line where the star is:
        #  ddd*ddd
        numbers.extend(parse_line(lines[i], pos))

        # now check line above and below
        #   d     d.d
        #   *      *
        for line0 in (lines[i - 1], lines[i + 1]):
            # case: there's a digit above the star
            if is_digit(line0[pos]):
                pos0 = pos
                # find the first digit
                while is_digit(line0[pos0]):
                    pos0 -= 1
                pos0 += 1
                # find the the number
                digits = ""
                while digit := is_digit(line0[pos0]):
                    pos0 += 1
                    digits += digit
                numbers.append(digits)
            # case: there's a dot or a symbol right above the star
            else:
                numbers.extend(parse_line(line0, pos))

        # here all numbers adjacent to the star are found
        print(f"{numbers=}")
        if len(numbers) == 2:
            print(f"Found a gear: {numbers=}")
            sum_gear_ratios += int(numbers[0]) * int(numbers[1])

print(f"{sum_gear_ratios=}")
