from concurrent.futures import ProcessPoolExecutor
from itertools import product

from pyaoc2019.utils import read_file, mapt, timer, chunks, exhaust
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False, cls=None):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return mapt(cls.from_str, read_file(filename, 2021))


class Rule:
    def __init__(self, set_val, funcs):
        self.set_val = set_val
        self.funcs = funcs

    def val(self, coord):
        return self.set_val if all(fn(v) for fn, v in zip(self.funcs, coord)) else None

    @classmethod
    def from_str(cls, s: str):
        t, rngs = s.split()
        set_val = t == 'on'

        def _check_func(start, end):
            return lambda v, start=start, end=end: start <= v <= end

        funcs = [_check_func(*eval(rng_str[2:].replace('..', ',')))
                 for rng_str in rngs.split(',')]
        return cls(set_val, funcs)


class Rules:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def __iter__(self):
        return iter(self.rules)

    def __getitem__(self, item):
        return self.rules[item]

    def __len__(self):
        return len(self.rules)

    def apply(self, c, init=0):
        cur = init
        for r in self:
            if (new_val := r.val(c)) is not None:
                cur = new_val
        return cur

    def apply_chunk(self, points):
        return [self.apply(p) for p in points]


def _test():
    rules = parse_data(debug=True)
    r = rules[0]
    c = 12, 12, 12
    print(r.val(c))

    print(sum(rules.apply(p) for p in product(range(-50, 51), repeat=3)))


@timer
def part1(rules):
    return sum(rules.apply(p) for p in product(range(-50, 51), repeat=3))


class Coord2(NamedTuple):
    x: int
    y: int


class LS(NamedTuple):
    """line segment"""
    min: int
    max: int

    @classmethod
    def from_str(cls, s):
        """x=2..4"""
        return LS(*eval(s[2:].replace('..', ',')))


class PS(NamedTuple):
    """plane segment"""


class Cube(NamedTuple):
    val: int
    x: LS
    y: LS
    z: LS

    @classmethod
    def from_str(cls, s: str):
        t, rngs = s.split()
        set_val = t == 'on'

        return cls(set_val, *map(LS.from_str, rngs.split(',')))


def part2(rules):
    pass


def __main():
    # return _test()
    # rules = Rules(parse_data(debug=True, cls=Rule))
    # print(len(rules))
    # print(part1(rules))
    cubes = parse_data(debug=True, cls=Cube)
    exhaust(print, cubes)
    # print(part2(rules))


if __name__ == '__main__':
    __main()
