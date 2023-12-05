EXAMPLE = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def card_points(card: tuple[list[int], list[int]]) -> int:
    n = len(set(card[1]).intersection(card[0]))
    return 0 if n == 0 else 2 ** (n - 1)


def parse_card(line: str) -> tuple[list[int], list[int]]:
    content = line.split(":")[1]

    def ns(s: str) -> list[int]:
        return [int(n) for n in s.strip().split()]

    return tuple(ns(s) for s in content.split("|"))


assert card_points(parse_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")) == 8

with open("4/input.txt") as f:
    print(sum(card_points(parse_card(line)) for line in f.readlines()))
