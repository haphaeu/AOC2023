import re

data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

with open("day07.txt") as f:
    data = f.read()


class Hand:
    """Class representing a hand of cards.
    J is Joker, and has lowest rank.
    """

    labels = "J23456789TQKA"

    # Regular expressions for each hand type.
    # Assume that higher types are matched first.

    # XXXXX|JXXXX|JJXXX|JJJXX|JJJJX
    five_of_a_kind = re.compile(r"(\w)\1{4}|J(\w)\2{3}|JJ(\w)\3{2}|JJJ(\w)\4|JJJJ\w")
    # XXXXY|JXXXY|JJXXY|JJJXY|JXYYY|JJXYY
    four_of_a_kind = re.compile(
        r".*(\w)\1{3}.*|J(\w)\2{2}.*|JJ(\w)\3.*|JJJ(\w).*|J\w(\w)\5{2}|JJ\w(\w)\6"
    )
    # XXYYY|XXXYY|XXJYY (not: JXYYY, JJXXY, JJXYY, JXXXY as it is a 4-kind)
    full_house = re.compile(r"((\w)\2\2(\w)\3|(\w)\4(\w)\5\5|J(\w)\6(\w)\7)")
    # XXXYZ|JXXYZ|JJXYZ|JXYYZ|JXYZZ
    three_of_a_kind = re.compile(
        r".*(\w)\1\1.*|J(\w)\2.*|JJ(\w).*|J\w(\w)\4\w|J\w\w(\w)\5"
    )
    # no joker in 2 pairs, as can always make a 3-of-kind.
    two_pair = re.compile(r".*(\w)\1.*(\w)\2.*")
    # XXYZW|JXYZW
    one_pair = re.compile(r".*(\w)\1.*|.*J(\w).*")

    types = {
        "five_of_a_kind": 9,
        "four_of_a_kind": 8,
        "full_house": 7,
        "three_of_a_kind": 6,
        "two_pair": 5,
        "one_pair": 4,
        "high_card": 3,
        "invalid": -1,
    }
    inv_types = {v: k for k, v in types.items()}

    def __init__(self, cards, bid) -> None:
        assert len(cards) == 5
        self.bid = bid
        self.cards = cards
        self.cards_sorted = "".join(sorted(self.cards, key=Hand.labels.index))
        self._type_value = self._get_type()
        self.type = Hand.inv_types[self._type_value]

    def __repr__(self) -> str:
        return f"Hand({self.cards}, {self.bid}, {self.type})"

    def __gt__(self, other):
        if self._type_value == other._type_value:
            # same types - compare card by card
            for c1, c2 in zip(self.cards, other.cards):
                if Hand.labels.index(c1) == Hand.labels.index(c2):
                    continue
                else:
                    return Hand.labels.index(c1) > Hand.labels.index(c2)
            # identical hands
            return False
        else:
            return self._type_value > other._type_value

    def _get_type(self):
        if Hand.five_of_a_kind.match(self.cards_sorted):
            return Hand.types["five_of_a_kind"]
        if Hand.four_of_a_kind.match(self.cards_sorted):
            return Hand.types["four_of_a_kind"]
        if Hand.full_house.match(self.cards_sorted):
            return Hand.types["full_house"]
        if Hand.three_of_a_kind.match(self.cards_sorted):
            return Hand.types["three_of_a_kind"]
        if Hand.two_pair.match(self.cards_sorted):
            return Hand.types["two_pair"]
        if Hand.one_pair.match(self.cards_sorted):
            return Hand.types["one_pair"]
        else:
            return Hand.types["high_card"]


hands = [
    Hand(cards, int(bid))
    for cards, bid in [line.split() for line in data.strip().splitlines()]
]

winning = 0
for i, hand in enumerate(sorted(hands)):
    winning += hand.bid * (i + 1)
print(f"{winning=}")
