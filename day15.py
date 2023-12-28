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


all_sum = 0
for seq in sequences:
    all_sum += hash(seq)
print(all_sum)
