import re

EXAMPLE = """
seeds: 79 14 55 13

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


def parse_seeds(seeds: str) -> list[int]:
    return [int(s) for s in seeds.split(":")[1].strip().split(" ")]


MAP_LINE_RE = re.compile("([a-z]+)-to-([a-z]+)")

Map = tuple[str, str, list[list[int]]]


def parse_map(map: str) -> Map:
    lines = map.strip().splitlines()
    from_attr, to_attr = MAP_LINE_RE.match(lines[0]).groups()
    mappings = [[int(s) for s in line.split(" ")] for line in lines[1:]]
    return from_attr, to_attr, mappings


def parse_input(input: str) -> tuple[list[int], list[Map]]:
    blocks = input.strip().split("\n\n")
    return (parse_seeds(blocks[0]), [parse_map(map) for map in blocks[1:]])


assert parse_seeds(EXAMPLE.strip().split("\n\n")[0]) == [79, 14, 55, 13]
assert parse_map(EXAMPLE.strip().split("\n\n")[1]) == (
    "seed",
    "soil",
    [[50, 98, 2], [52, 50, 48]],
)
assert len(parse_input(EXAMPLE)[1]) == 7


def find_seed_location(seed: int, maps: list[Map]) -> int:
    map_cursor = "seed"
    value_cursor = seed

    while map_cursor != "location":
        map = next(map for map in maps if map[0] == map_cursor)

        for dest_start, source_start, range_size in map[2]:
            diff = value_cursor - source_start
            if diff > 0 and diff < range_size:
                value_cursor = dest_start + diff
                break

        # If not found, value cursor is not changed

        map_cursor = map[1]

    return value_cursor


assert find_seed_location(79, parse_input(EXAMPLE)[1]) == 82

with open("5/input.txt") as f:
    seeds, maps = parse_input(f.read())
    seed_locations = [find_seed_location(seed, maps) for seed in seeds]
    print(min(seed_locations))
