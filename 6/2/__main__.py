import functools
from math import ceil, floor, sqrt


EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200
"""


def parse_input(input: str) -> list[tuple[int, int]]:
    split = input.strip().splitlines()
    time = int("".join(split[0].split(":")[1].strip().split()))
    distance = int("".join(split[1].split(":")[1].strip().split()))
    return [(time, distance)]


print(parse_input(EXAMPLE))
assert parse_input(EXAMPLE) == [(71530, 940200)]

# The equation for the line representing distance over time for hold time s is:
# d = s * (t - s)
# That is, a line from the origin shifted right by s

# The distance travelled in a time T is:
# d = s * (T - s) = Ts - s^2

# So it's an upside-down parabola.
# Now let's take D to be the record distance.
# To find the values of s that produce d > D, we only need to find the first
# value that produces d > D then the first value after that value that produces d < D,
# since we know the parabola will only cross a once. We can do this by finding
# the roots of:
# d = Ts - s^2 - D


def roots(D: int, T: int) -> tuple[float, float]:
    a = -1
    b = T
    c = -D
    determinant = sqrt(b**2 - 4 * a * c)
    return ((-b + determinant) / (2 * a), (-b - determinant) / (2 * a))


def num_winning_times(D: int, T: int) -> int:
    (lower, upper) = roots(D, T)
    lower_quanitized = max(0, floor(lower + 1))
    upper_quantized = min(ceil(upper - 1), T)
    return upper_quantized - lower_quanitized + 1


def calc_answer(races: list[tuple[int, int]]) -> int:
    return functools.reduce(
        lambda x, y: x * y, (num_winning_times(D, T) for T, D in races), 1
    )


with open("6/input.txt") as f:
    print(calc_answer(parse_input(f.read())))
