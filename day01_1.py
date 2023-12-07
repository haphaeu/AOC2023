import requests
import re


# data = """1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet""".split(
#     "\n"
# )
# Answer: 142


with open("day01.txt") as f:
    data = f.readlines()

pattern = r"(\d)"

code = 0
for line in data:
    matches = re.findall(pattern, line)
    if matches:
        code += 10 * int(matches[0]) + int(matches[-1])
print(code)

# Output: Your puzzle answer was 55477.
