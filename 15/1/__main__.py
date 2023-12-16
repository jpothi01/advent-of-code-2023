EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

Step = str


def parse_input(input: str) -> list[Step]:
    return input.replace("\n", "").split(",")


def hash(step: Step) -> int:
    current_value = 0

    for c in step:
        current_value += ord(c)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value


def hash_steps(steps: list[Step]) -> list[int]:
    hashes: list[int] = []
    for step in steps:
        hashes.append(hash(step))

    return hashes


assert hash("rn=1") == 30
assert sum(hash_steps(parse_input(EXAMPLE))) == 1320

with open("15/input.txt") as f:
    print(sum(hash_steps(parse_input(f.read()))))
