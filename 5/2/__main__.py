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


def find_min_seed_location(
    map_cursor: str,
    range_start: int,
    range_size: int,
    maps: list[Map],
    min_location: int,
) -> int:
    map = next(map for map in maps if map[0] == map_cursor)

    unmapped_ranges = [(range_start, range_start + range_size - 1)]
    next_map_cursor = map[1]

    print(f"ranges: {(range_start, range_start + range_size)}")
    for dest_start, source_start, dest_range_size in map[2]:
        source_end = source_start + dest_range_size - 1
        range_end = range_start + range_size - 1

        if range_start <= source_end and range_end >= source_start:
            print(
                f"found {map_cursor}: {(range_start, range_end, source_start, source_end)}"
            )
            match_source_start = max(range_start, source_start)
            chunk_start = dest_start + (match_source_start - source_start)
            chunk_end = (
                min(
                    dest_start + dest_range_size,
                    chunk_start + range_size - (match_source_start - range_start),
                )
                - 1
            )
            chunk_size = chunk_end - chunk_start + 1
            assert chunk_size > 0 and chunk_size <= dest_range_size

            if next_map_cursor == "location":
                # Start of the chunk is the smallest
                assert chunk_start != 0
                min_location = min(min_location, chunk_start)
            else:
                min_location = find_min_seed_location(
                    next_map_cursor, chunk_start, chunk_size, maps, min_location
                )

            # print((source_start, source_start + dest_range_size))
            # print(mapped_range_start)
            # print(mapped_range_start + chunk_size)
            index = -1
            print(
                f"finding {map_cursor}: {match_source_start} {match_source_start + chunk_size - 1}"
            )
            print(f"unmapped_ranges {map_cursor}: {unmapped_ranges}")
            found_range = None
            for i, range in enumerate(unmapped_ranges):
                if range[1] < range[0]:
                    continue
                if (
                    match_source_start >= range[0]
                    and match_source_start + chunk_size - 1 <= range[1]
                ):
                    index = i
                    found_range = range
                    break

            # print((dest_start, source_start, dest_range_size))
            if index == -1:
                raise Exception()

            unmapped_ranges[index] = (match_source_start + chunk_size, found_range[1])
            unmapped_ranges.insert(index, (found_range[0], match_source_start - 1))

    # print(unmapped_ranges)
    for range in unmapped_ranges:
        if range[1] < range[0]:
            continue
        if next_map_cursor == "location":
            # Start of the chunk is the smallest
            assert range[0] != 0
            min_location = min(min_location, range[0])
        else:
            min_location = find_min_seed_location(
                next_map_cursor, range[0], range[1] - range[0] + 1, maps, min_location
            )

    print("returning")
    return min_location


# assert find_seed_location(79, parse_input(EXAMPLE)[1]) == 82

with open("5/input.txt") as f:
    seeds, maps = parse_input(f.read())
    # seeds, maps = parse_input(EXAMPLE)
    seed_ranges = [seeds[i * 2 : i * 2 + 2] for i in range(int(len(seeds) / 2))]

    min_location = 1_000_000_000
    for seed_range in seed_ranges:
        min_location = min(
            min_location,
            find_min_seed_location(
                "seed", seed_range[0], seed_range[1], maps, min_location
            ),
        )

    print(min_location)
