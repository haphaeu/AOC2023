import time

from day05_1 import data_example, data_full, a2b_maps_names, Almanac, parse_A2B_Maps


def get_pairs(lines):
    for line in lines:
        if "seeds:" in line:
            break
    values = [int(x) for x in line.split(":")[1].split()]
    starts = values[::2]
    lengths = values[1::2]
    return starts, lengths


def parse_seeds2(lines):
    starts, lengths = get_pairs(lines)
    for s, l in zip(starts, lengths):
        for i in range(l):
            yield s + i


def check_overlap(lines):
    starts, lengths = get_pairs(lines)
    for s1, l1 in zip(starts, lengths):
        e1 = s1 + l1
        for s2, l2 in zip(starts, lengths):
            e2 = s2 + l2
            if s1 < s2 < e1 or s1 < e2 < e1:
                return True
    return False


def main():
    data = data_full
    lines = data.splitlines()

    a2b_maps = [parse_A2B_Maps(lines, name) for name in a2b_maps_names]
    almanac = Almanac(a2b_maps)

    print("Tracing...")
    seeds = parse_seeds2(lines)
    min_location = 99999999999999
    for i, seed in enumerate(seeds):
        location = almanac.trace(seed, verbose=False)
        if location < min_location:
            min_location = location
            print()
        print(f"{i:_} Minimum location: {min_location}", end="\r")
    print()


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"et: {time.time() - t0:.3f}s")

# Output: 59370572 (run hadn't finish yet, was running overnight...)
