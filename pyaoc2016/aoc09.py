from contextlib import suppress
from functools import partial
from typing import Callable, NamedTuple
from pyaoc2019.utils import read_file
from operator import mul, floordiv

__author__ = 'acushner'

data = read_file(9, 2016)[0]


def skip(iterable, n) -> None:
    for _ in range(n):
        next(iterable)


def decompress_len_v1(s: str) -> int:
    it = enumerate(s)
    total = 0
    with suppress(StopIteration):
        while True:
            idx, c = next(it)
            if c != '(':
                total += 1
                continue
            end = s.find(')', idx)
            num_chars, num_repeat = map(int, s[idx + 1 : end].split('x'))
            total += num_chars * num_repeat
            skip(it, num_chars + end - idx)
    return total


def test_v1():
    vals = (
        ('ADVENT', 6),
        ('A(1x5)BC', 7),
        ('(3x3)XYZ', 9),
        ('A(2x2)BCD(2x2)EFG', 11),
        ('(6x1)(1x3)A', 6),
        ('X(8x2)(3x3)ABCY', 18),
    )

    def _test(s, l):
        res = decompress_len_v1(s)
        assert res == l, f'{s=} {res=} {l=}'

    for v in vals:
        _test(*v)


def part1():
    test_v1()
    return decompress_len_v1(data)


def test_v2():
    vals = (
        ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
        ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
    )

    def _test(s, l):
        res = decompress_len_v2(s)
        assert res == l, f'{s=} {res=} {l=}'

    for v in vals:
        _test(*v)


def decompress_len_v2(s: str, mult=1) -> int:
    it = enumerate(s)
    total = 0
    for idx, c in it:
        if c != '(':
            total += mult
            continue

        end = s.find(')', idx)
        num_chars, num_repeat = map(int, s[idx + 1 : end].split('x'))
        skip(it, num_chars + end - idx)
        sub_str = s[end + 1 : end + num_chars + 1]
        total += decompress_len_v2(sub_str, mult * num_repeat)

    return total


def part2():
    test_v2()
    return decompress_len_v2(data)


def __main():
    # print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
