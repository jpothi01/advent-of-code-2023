from typing import Optional


sum = 0

def calibration_value(line: str) -> int:
    first_digit: Optional[str] = None
    last_digit: Optional[str] = None

    for char in line:
        if char.isdigit():
            if not first_digit:
                first_digit = char

            last_digit = char

    assert first_digit and last_digit
    return int(first_digit + last_digit)

with open("1/input.txt") as f:
    for line in f.readlines():
        sum += calibration_value(line)

print(sum)