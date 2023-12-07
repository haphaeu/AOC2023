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

# find all symbols
pattern_symbols = re.compile(r"[^\d.\n]")
symbols = list(set(pattern_symbols.findall(schematic)))
print(f"{symbols=}")

# find all numbers
pattern_numbers = re.compile(r"\d+")

lines = schematic.splitlines(keepends=True)
sum_part_numbers = 0
schematic_parts = []
for i, line in enumerate(lines):
    print(i)
    print("".join(lines[max(i - 1, 0) : i + 2]))
    numbers = pattern_numbers.findall(line)
    schematic_line = line[:]
    for number in numbers:
        start, stop = re.search(r"\b{}\b".format(number), line).span()
        slc = slice(max(start - 1, 0), min(stop + 1, len(line)))
        is_part_number = any(
            [
                any(symbol in li[slc] for symbol in symbols)
                for li in lines[max(i - 1, 0) : i + 2]
            ]
        )
        if is_part_number:
            sum_part_numbers += int(number)
            schematic_line = schematic_line.replace(number, "T" * len(number), 1)
        else:
            schematic_line = schematic_line.replace(number, "F" * len(number), 1)

        print(number, is_part_number)
    schematic_parts.append(schematic_line)

# Only false-positive duplicate number is 787, easily found by
#     if len(numbers) > len(set(numbers)):
#         print(i, line)
print(sum_part_numbers - 787)

with open("day03_check.txt", "w") as f:
    f.write("".join(schematic_parts))  # .replace(".", " "))
