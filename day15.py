from __future__ import annotations
from typing import Any, List
import re


data = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""".strip()

data = open("day15.txt").read().strip()

sequences = data.split(",")


def hash(word):
    hash = 0
    for c in word:
        hash = (hash + ord(c)) * 17 % 256
    return hash


# Part 1
all_sum = 0
for seq in sequences:
    all_sum += hash(seq)
print(all_sum)

# Part 2

# 256 boxes numbered from 0 to 255
# focal lengths from 1 to 9
# each sequence indicates the label of the lens on which the step operates.
# running the hash on the label indicates which box to use
# the label is immediately followed by = or -
# - means remove the lens from the box if it is present, and shift the remaining lenses forward
# = will be followed by a number indicating focal length, which is then added to the box
# be sure to label the lens, then, if there is already such label, replace it.


class Lens:
    def __init__(self, label: str, focal_length: int):
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, __value: Lens) -> bool:
        return self.label == __value.label

    def __repr__(self) -> str:
        return f"{self.label} {self.focal_length}"


class LensesList(List):
    def __init__(self, lenses: List[Lens]):
        self.lenses = lenses

    def __repr__(self) -> str:
        return self.lenses.__repr__()

    def remove(self, label: str):
        for lens in self.lenses:
            if lens.label == label:
                self.lenses.remove(lens)
                return

    def add(self, label: str, focal_length: int):
        for lens in self.lenses:
            if lens.label == label:
                lens.focal_length = focal_length
                return
        lens = Lens(label, focal_length)
        self.lenses.append(lens)


class Box:
    def __init__(self, idx: int, lenses_list: LensesList = None):
        self.idx = idx
        if lenses_list is None:
            self.lenses_list = LensesList([])
        else:
            self.lenses_list = lenses_list

    def __repr__(self) -> str:
        return f"Box {self.idx}: {self.lenses_list}"

    def remove(self, label: str):
        self.lenses_list.remove(label)

    def add(self, label: str, focal_length: int):
        self.lenses_list.add(label, focal_length)

    def is_empty(self):
        return len(self.lenses_list.lenses) == 0

    def focus_power(self):
        n = self.idx + 1
        lenses = self.lenses_list.lenses
        return sum([n * (i + 1) * lens.focal_length for i, lens in enumerate(lenses)])


class Operate:
    def __init__(self, boxes: List[Box]):
        self.boxes = boxes

    def __call__(self, seq):
        """
        cm=1: add/replace 'cm' to box hash('cm')
        pq- : remove 'pq' from box hash('pq')
        """
        label, focal_length = re.split("=|-", seq)
        box_idx = hash(label)
        box = self.boxes[box_idx]

        if "-" in seq:
            box.remove(label)
        elif "=" in seq:
            focal_length = int(focal_length)
            box.add(label, focal_length)

    def focus_power(self):
        return sum([box.focus_power() for box in self.boxes])

    def show(self):
        for box in self.boxes:
            if not box.is_empty():
                print(box)


boxes = [Box(i) for i in range(256)]
oper = Operate(boxes)
for seq in sequences:
    oper(seq)
print(f"After {seq}:")
oper.show()
print(oper.focus_power())
