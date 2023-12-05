from typing import Optional


EXAMPLE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def is_symbol(c: str) -> bool:
    return not c.isdigit() and c != "."


def gather_gears(schematic: str) -> list[tuple[int, int]]:
    lines = schematic.strip().splitlines()

    # number, start, end (inclusive)
    part_number_coordinates: list[tuple[int, tuple[int, int], tuple[int, int]]] = []

    # Get the numbers
    for row, line in enumerate(lines):
        number_buf = ""

        for col, char in enumerate(line):
            if char.isdigit():
                number_buf += char
            else:
                if number_buf:
                    part_number_coordinates.append(
                        (
                            int(number_buf),
                            (row, col - len(number_buf)),
                            (row, col - 1),
                        )
                    )
                number_buf = ""

        if number_buf:
            part_number_coordinates.append(
                (
                    int(number_buf),
                    (row, col - len(number_buf)),
                    (row, len(line) - 1),
                )
            )

    # Figure out which ones have adjacency
    test_offsets = [
        (0, 1),
        (0, -1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    def gear_numbers(gear_row: int, gear_col: int) -> Optional[tuple[int, int]]:
        nonlocal part_number_coordinates

        ns: list[int] = []

        for number, start, end in part_number_coordinates:
            found = False
            for offset_row, offset_col in test_offsets:
                test_row = start[0]
                for test_col in range(start[1], end[1] + 1):
                    if (test_row, test_col) == (
                        gear_row + offset_row,
                        gear_col + offset_col,
                    ):
                        ns.append(number)
                        found = True
                        break

                if found:
                    break

        if len(ns) == 2:
            return tuple(ns)

        return None

    gears: list[tuple[int, int]] = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "*":
                if ns := gear_numbers(row, col):
                    gears.append(ns)

    return gears


print(gather_gears(EXAMPLE))
assert gather_gears(EXAMPLE) == [(467, 35), (755, 598)]

with open("3/input.txt") as f:
    gears = gather_gears(f.read())

print(sum(x * y for x, y in gears))
