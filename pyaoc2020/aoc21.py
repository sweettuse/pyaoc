from collections import Counter, defaultdict
from functools import reduce
from operator import itemgetter
from typing import Set, NamedTuple

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


class Info(NamedTuple):
    ings: Set[str]
    allergens: Set[str]

    @classmethod
    def from_str(cls, s: str):
        ings, allergens = s.split(' (contains ')
        ings = set(ings.split())
        allergens = set(allergens[:-1].split(', '))
        return cls(ings, allergens)


def _parse_data(fname=21):
    return [Info.from_str(s) for s in read_file(fname, 2020)]


def _get_all_ings_allergen_map(fname=21):
    all_ings = Counter()
    allergen_map = {}
    for ings, allergens in _parse_data(fname):
        all_ings.update(ings)
        for a in allergens:
            if a not in allergen_map:
                allergen_map[a] = ings.copy()
            else:
                allergen_map[a] &= ings
    return all_ings, allergen_map


def part1():
    all_ings, allergen_map = _get_all_ings_allergen_map()
    with_allergens = reduce(set.union, allergen_map.values())
    return sum(v for k, v in all_ings.items() if k not in with_allergens)


def part2():
    _, allergen_map = _get_all_ings_allergen_map()
    ing_allergen_map = defaultdict(set)
    for a, ings in allergen_map.items():
        for i in ings:
            ing_allergen_map[i].add(a)

    res = []
    while ing_allergen_map:
        cur_ing, cur_a = min(ing_allergen_map.items(), key=lambda kv: len(kv[1]))
        ing_allergen_map.pop(cur_ing)
        for v in ing_allergen_map.values():
            v -= cur_a
        res.append((cur_a.pop(), cur_ing))

    res.sort()
    return ','.join(map(itemgetter(1), res))


@timer
def __main():
    print(part1())
    print(part2())


# 2265
# dtb,zgk,pxr,cqnl,xkclg,xtzh,jpnv,lsvlx
# '__main' took 0.002233622999999997 seconds


if __name__ == '__main__':
    __main()
