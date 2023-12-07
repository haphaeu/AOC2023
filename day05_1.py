class SubMap:
    """SubMap class for mapping one value to another.
    Represents a single range of values:
    """

    def __init__(self, dst_start, src_start, length):
        self.dst_start = dst_start
        self.src_start = src_start
        self.src_end = src_start + length - 1
        self.length = length

    def __call__(self, x):
        if not self.valid_range(x):
            raise ValueError(f"Value {x} not in range of {self}")
        return x - self.src_start + self.dst_start

    def __repr__(self):
        return f"SubMap({self.dst_start}, {self.src_start}, {self.length})"

    def valid_range(self, x):
        return x >= self.src_start and x <= self.src_end


class A2B_Maps:
    """A2B_Maps class for mapping one value to another.
    Represents all SubMaps for the same A-to-B classes:
    """

    def __init__(self, name, maps):
        self.name = name
        self.maps = maps

    def __call__(self, x):
        for m in self.maps:
            if m.valid_range(x):
                return m(x)
        # Any source numbers that aren't mapped correspond to the same
        # destination number. So, seed number 10 corresponds to soil number 10.
        return x

    def __repr__(self) -> str:
        return f"A2B_Maps({self.name}, {self.maps})"


class Almanac:
    def __init__(self, map_collection):
        self.map_collection = map_collection

    def __repr__(self) -> str:
        return f"Almanac({self.map_collection})"

    def trace(self, x, verbose=True):
        if verbose:
            print(f"seed: {x}")
        for m in self.map_collection:
            x = m(x)
            if verbose:
                print(f"{m.name}: {x}")
        return x


def parse_seeds(lines):
    for line in lines:
        if "seeds:" in line:
            return [int(x) for x in line.split(":")[1].split()]


def parse_A2B_Maps(lines, map_name):
    print(f'Parsing "{map_name}"')
    for i, line in enumerate(lines):
        if map_name in line:
            break
    maps = []
    while True:
        i += 1
        sub_line = lines[i]
        try:
            print(sub_line)
            maps.append(SubMap(*(int(x) for x in sub_line.split())))
        except (ValueError, TypeError):
            break
        if i == len(lines) - 1:
            break
    return A2B_Maps(map_name, maps)


a2b_maps_names = [
    "seed-to-soil map",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]

data_example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

with open("day05.txt") as f:
    data_full = f.read()


def main():
    data = data_example

    lines = data.splitlines()

    a2b_maps = [parse_A2B_Maps(lines, name) for name in a2b_maps_names]
    almanac = Almanac(a2b_maps)

    seeds = parse_seeds(lines)
    min_location = 99999999999999
    for seed in seeds:
        location = almanac.trace(seed)
        if location < min_location:
            min_location = location
        print()
    print(f"Minimum location: {min_location}")


if __name__ == "__main__":
    main()
