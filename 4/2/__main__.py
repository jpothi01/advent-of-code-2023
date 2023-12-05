EXAMPLE = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

Card = list[int], list[int]


def num_matches(card: tuple[list[int], list[int]]) -> int:
    return len(set(card[1]).intersection(card[0]))


def parse_card(line: str) -> tuple[list[int], list[int]]:
    content = line.split(":")[1]

    def ns(s: str) -> list[int]:
        return [int(n) for n in s.strip().split()]

    return tuple(ns(s) for s in content.split("|"))


def parse_cards(input: str) -> list[Card]:
    return [parse_card(line) for line in input.strip().splitlines()]


def card_count(cards: list[Card]) -> int:
    card_counts: list[int] = [1 for _ in cards]

    for i, card in enumerate(cards):
        matches = num_matches(card)
        num_copies = card_counts[i]

        for j in range(matches):
            if i + j + 1 < len(card_counts):
                card_counts[i + j + 1] += num_copies

    return sum(card_counts)


assert card_count(parse_cards(EXAMPLE)) == 30

with open("4/input.txt") as f:
    print(card_count([parse_card(line) for line in f.readlines()]))
