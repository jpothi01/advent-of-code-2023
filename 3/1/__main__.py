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


def gather_part_numbers(schematic: str) -> list[int]:
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

    def is_part_number(start: tuple[int, int], end: tuple[int, int]) -> bool:
        row = start[0]
        for col in range(start[1], end[1] + 1):
            for offset_row, offset_col in test_offsets:
                test_row, test_col = row + offset_row, col + offset_col
                if (
                    test_row >= 0
                    and test_col >= 0
                    and test_row < len(lines)
                    and test_col < len(lines[0])
                    and is_symbol(lines[test_row][test_col])
                ):
                    return True

        return False

    part_numbers: list[int] = []
    for number, start, end in part_number_coordinates:
        if is_part_number(start, end):
            part_numbers.append(number)

    return part_numbers


assert gather_part_numbers(EXAMPLE) == [467, 35, 633, 617, 592, 755, 664, 598]

with open("3/input.txt") as f:
    part_numbers = gather_part_numbers(f.read())

print(sum(part_numbers))
