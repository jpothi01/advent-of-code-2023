from typing import Literal
import re

EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

Op = Literal["-", "="]
Step = tuple[str, Op, int]
Lens = tuple[str, int]


def parse_input(input: str) -> list[Step]:
    STEP_RE = re.compile(r"^([^=-]+)([=-])(\d+)?")

    def parse_step(step: str) -> Step:
        match = STEP_RE.match(step)
        return (match.group(1), match.group(2), int(match.group(3) or "0"))

    return [parse_step(step) for step in input.replace("\n", "").split(",")]


def hash(step: Step) -> int:
    current_value = 0

    for c in step:
        current_value += ord(c)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value


def run_initialization_sequence(steps: list[Step]) -> dict[int, list[Lens]]:
    boxes: dict[int, list[Lens]] = {}

    for label, op, focal_length in steps:
        box_index = hash(label)
        # print(boxes)
        # print((label, op, focal_length, box_index))

        boxes.setdefault(box_index, [])

        if op == "=":
            insert_index = None
            for i, (other_label, _) in enumerate(boxes[box_index]):
                if other_label == label:
                    insert_index = i
                    break

            if insert_index is not None:
                boxes[box_index][insert_index] = (label, focal_length)
            else:
                boxes[box_index].append((label, focal_length))
        else:
            delete_index = -1
            for i, (other_label, _) in enumerate(boxes[box_index]):
                if other_label == label:
                    delete_index = i

            if delete_index != -1:
                del boxes[box_index][delete_index]

    return boxes


def focusing_power(boxes: dict[int, list[Lens]]) -> int:
    power = 0

    for box_index, lenses in boxes.items():
        for i, (_, focal_length) in enumerate(lenses):
            power += (box_index + 1) * (i + 1) * focal_length

    return power


with open("15/input.txt") as f:
    print(focusing_power(run_initialization_sequence(parse_input(f.read()))))

assert focusing_power(run_initialization_sequence(parse_input(EXAMPLE))) == 145
