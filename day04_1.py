data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

with open("day04.txt") as f:
    data = f.read()


def parse_card(card):
    """Card format is
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    First set is winning numbers, second is your game.
    First match gives 1 point, further matches doubles the points.
    """
    win, play = card.split(":")[1].split("|")
    win = set([int(x) for x in win.split()])
    play = [int(x) for x in play.split()]
    matches = win.intersection(play)
    if matches:
        return 2 ** (len(matches) - 1)
    return 0


print(sum([parse_card(card) for card in data.split("\n") if card]))
