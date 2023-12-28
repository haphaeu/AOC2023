"""
Copying from:
https://gist.github.com/rakslice/b596a1d3857c08d0412f0e2eace578b0
"""


def contents(filename):
    with open(filename, "r") as handle:
        return handle.read().strip()


memo = {}


def solver_rec(puz, scores):
    key = puz, tuple(scores)
    if key in memo:
        return memo[key]

    out = solver_rec_inner(puz, scores)
    memo[key] = out

    return out


def solver_rec_inner(puz, scores):
    hashes_left = sum(scores)
    if len(puz) < hashes_left:
        return 0

    if puz == "":
        if hashes_left > 0:
            return 0
        else:
            return 1

    if puz[0] == ".":
        return solver_rec(puz[1:], scores)

    if puz[0] == "#":
        # consume with score
        if len(scores) == 0:
            return 0
        cur_score = scores[0]
        rest = scores[1:]

        for i in range(cur_score):
            if puz[i] == ".":
                return 0
        if len(puz) == cur_score and rest == []:
            return 1
        if puz[cur_score] == "#":
            return 0  # must be dot

        return solver_rec(puz[cur_score + 1 :], rest)

    if puz[0] == "?":
        hash_count = 0
        q_count = 0
        for ch in puz:
            if ch == "?":
                q_count += 1
            if ch == "#":
                hash_count += 1

        if q_count + hash_count > hashes_left:
            return solver_rec("#" + puz[1:], scores) + solver_rec("." + puz[1:], scores)
        else:
            return solver_rec("#" + puz[1:], scores)

    assert False, "unreachable"


def problem(filename):
    input = contents(filename).split("\n")
    input = [x for x in input]

    cur = 0
    for x in input:
        zpuz, zscore = x.split(" ", 1)

        multi = 5
        puz = []
        score = []
        for i in range(multi):
            puz.append(zpuz)
            score.append(zscore)
        puz = "?".join(puz)
        score = ",".join(score)

        # print(puz, score)

        score = [int(x) for x in score.split(",")]

        combs = solver_rec(puz, score)

        # print(puz, combs)
        cur += combs

    return cur


def main():
    print(problem("day12.txt"))


if __name__ == "__main__":
    main()
