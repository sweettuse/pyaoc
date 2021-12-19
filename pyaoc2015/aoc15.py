from decimal import Decimal
from itertools import pairwise, product
from math import floor, ceil, prod

from pyaoc2019.utils import read_file, mapt, timer
from typing import NamedTuple

__author__ = 'acushner'


class Ing(NamedTuple):
    name: str
    cap: int
    dur: int
    flavor: int
    texture: int
    cals: int

    @classmethod
    def from_str(cls, s):
        t = s.replace(',', '').split()
        return cls(t[0][:-1], *map(int, t[2::2]))

    def __mul__(self, other):
        return type(self)('mul', *(other * v for v in self[1:]))

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        return type(self)('add', *(v1 + v2 for v1, v2 in zip(self[1:], other[1:])))


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return [Ing.from_str(s) for s in read_file(filename, 2015)]


def _create_constraints(const: Ing, other: Ing):
    vals = zip(const, other)
    next(vals)
    c_neg_ratios = set()
    c_pos_ratios = set()
    for c, o in vals:
        if not o:
            continue
        if c < 0 < o:
            add_to = c_neg_ratios
        elif o < 0 < c:
            add_to = c_pos_ratios
        else:
            continue
        add_to.add(-c / Decimal(o))

    return max(c_neg_ratios, default=0), min(c_pos_ratios, default=0)


def _get_possible_amounts(n, min_ratio: Decimal, max_ratio: Decimal):
    if not min_ratio:
        start = 0
    else:
        start = floor(n * min_ratio) + 1

    if not max_ratio:
        end = 100 - n
    else:
        end = min(100 - n, ceil(n * max_ratio) - 1)

    yield from range(start, end + 1)


def _my_sum(vals):
    return max(0, sum(vals))


def _calc_value(amounts, ings, max_cals=None):
    if sum(amounts) != 100:
        return 0
    total = [a * i for a, i in zip(amounts, ings)]
    by_asset = zip(*total)
    next(by_asset)
    *by_asset, cals = by_asset
    if max_cals and sum(cals) != 500:
        return 0
    return prod(map(_my_sum, by_asset))


def _create_combos(const, ratios):
    other, ratios = next(iter(ratios.items()))
    res = 0
    # for n in range(20, 22):
    for n in range(1, 100):
        for other_n in _get_possible_amounts(n, *ratios):
            res = max(res, _calc_value((n, other_n), (const, other)))

    return res


def _find_best_combo(const, ratios, max_cals=None):
    ratios = iter(ratios.items())
    o1, r1 = next(ratios)
    o2, r2 = next(ratios)
    o3, r3 = next(ratios)
    res = 0
    # for n in range(20, 22):
    total_checked = 0
    for n in range(100):
        for on1 in _get_possible_amounts(n, *r1):
            for on2 in _get_possible_amounts(n, *r2):
                for on3 in _get_possible_amounts(n, *r3):
                    total_checked += 1
                    res = max(res, _calc_value((n, on1, on2, on3), (const, o1, o2, o3), max_cals))

    print(100 ** 4 / total_checked)
    return res


@timer
def _find_best_combos_brute(ings, max_cals=None):
    res = 0
    for ns in product(range(100), repeat=len(ings)):
        res = max(res, _calc_value(ns, ings, max_cals))
    return res


@timer
def parts1and2(data, max_cals=None):
    const, *rest = data
    ratios = {o: _create_constraints(const, o) for o in rest}
    return _find_best_combo(const, ratios, max_cals)


def __main():
    data = parse_data(debug=False)
    # print(parts1and2(data))
    # print(parts1and2(data, 500))
    print(_find_best_combos_brute(data))
    print(_find_best_combos_brute(data, 500))


if __name__ == '__main__':
    __main()
