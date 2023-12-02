from __future__ import annotations
from itertools import count
import string

from rich import print
from pyaoc2019.utils import read_file


def part1(path="01.txt"):
    return sum(map(_get_cal, map(_to_ints, read_file(path))))


def _to_ints(l):
    return (int(c) for c in l if c.isdigit())


def _get_cal(ints):
    ints = list(ints)
    match len(ints):
        case 0:
            raise Exception
        case 1:
            a = b = ints[0]
        case _:
            a, b = ints[0], ints[-1]
    return 10 * a + b


def part2(path="01.txt"):
    return sum(map(_get_cal2, read_file(path)))


_number_map = dict(zip(string.digits, count()))
number_name_map = (
    dict(zip("one two three four five six seven eight nine".split(), count(1)))
    | _number_map
)


def _get_cal2(l: str) -> int:
    return _get_cal((_get_number(l), _get_number(l, reverse=True)))


def _get_number(l: str, *, reverse=False):
    agg, find = min, str.find
    if reverse:
        agg, find = max, str.rfind

    idx_vals = (
        (idx, val)
        for name, val in number_name_map.items()
        if (idx := find(l, name)) != -1
    )
    return agg(idx_vals)[1]


def __main():
    print(part1(), part2())


if __name__ == "__main__":
    __main()
