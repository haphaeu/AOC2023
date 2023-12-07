import re

# data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# """.split(
#     "\n"
# )
# # # Output: 2286

with open("day02.txt", "r") as f:
    data = f.read().split("\n")
# # Output: 67953

pattern_game_id = re.compile(r"Game (\d+):.*")
pattern_red = re.compile(r"(\d+) red")
pattern_green = re.compile(r"(\d+) green")
pattern_blue = re.compile(r"(\d+) blue")


def parse_draw(draw):
    try:
        red = int(pattern_red.findall(draw)[0])
    except IndexError:
        red = 0
    try:
        green = int(pattern_green.findall(draw)[0])
    except IndexError:
        green = 0
    try:
        blue = int(pattern_blue.findall(draw)[0])
    except IndexError:
        blue = 0
    return red, green, blue


def parse_game(line):
    game_id = int(pattern_game_id.match(line).group(1))
    line = line.replace(f"Game {game_id}: ", "")
    draws = line.split(";")
    r, g, b = 0, 0, 0
    for draw in draws:
        ri, gi, bi = parse_draw(draw)
        r = max(r, ri)
        g = max(g, gi)
        b = max(b, bi)

    power = r * g * b

    print(f"Game {game_id} power is: {power}")
    return power


sum_power = 0
for line in data:
    if not line:
        continue
    sum_power += parse_game(line)

print(f"Sum of powers: {sum_power}")
