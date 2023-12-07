from collections import defaultdict

data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

with open("day04.txt") as f:
    data = f.read()


def parse_card2(card):
    """Card format is
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    First set is winning numbers, second is your game.
    Returns the number of matches.
    """
    card_id = int(card.split(":")[0].split()[1])
    win, play = card.split(":")[1].split("|")
    win = set([int(x) for x in win.split()])
    play = set([int(x) for x in play.split()])
    return card_id, len(win.intersection(play))


# keep cards count
d = defaultdict(int)

for card in data.splitlines():
    card_id, num_matches = parse_card2(card)
    d[card_id] += 1
    for i in range(num_matches):
        d[card_id + i + 1] += d[card_id]

print(sum(d.values()))
