from typing import Optional


SPELLED_DIGIT_TABLE = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]

def calibration_value(line: str) -> int:
    first_digit: Optional[str] = None
    last_digit: Optional[str] = None
    spelled_digit_cursors: list[int] = [0 for _ in SPELLED_DIGIT_TABLE]

    def capture_digit(digit: str):
        nonlocal first_digit
        nonlocal last_digit

        if not first_digit:
            first_digit = digit

        last_digit = digit

    for char in line:
        if char.isdigit():
            capture_digit(char)

            for i in range(len(SPELLED_DIGIT_TABLE)):
                spelled_digit_cursors[i] = 0
        else:
            for digit_index, digit_str in enumerate(SPELLED_DIGIT_TABLE):
                if char == digit_str[spelled_digit_cursors[digit_index]]:
                    spelled_digit_cursors[digit_index] += 1
                    if spelled_digit_cursors[digit_index] == len(digit_str):
                        capture_digit(str(digit_index + 1))
                        spelled_digit_cursors[digit_index] = 0
                else:
                    spelled_digit_cursors[digit_index] = 1 if char == digit_str[0] else 0

    assert first_digit and last_digit
    return int(first_digit + last_digit)

sum = 0

with open("1/2/input.txt") as f:
    for line in f.readlines():
        sum += calibration_value(line)

assert calibration_value("two1nine") == 29
assert calibration_value("eightwothree") == 83
assert calibration_value("abcone2threexyz") == 13
assert calibration_value("xtwone3four") == 24
assert calibration_value("4nineeightseven2") == 42
assert calibration_value("zoneight234") == 14
assert calibration_value("7pqrstsixteen") == 76
assert calibration_value("1ttwo") == 12

print(sum)