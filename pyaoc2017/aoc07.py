from collections import Counter
from itertools import chain
from operator import attrgetter, itemgetter
from typing import NamedTuple, FrozenSet

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


class ResultException(Exception):
    """contains result"""


class ProgInfo(NamedTuple):
    name: str
    weight: int
    children: FrozenSet[str]

    @classmethod
    def from_str(cls, s):
        l, *r = s.split(' -> ')
        name, weight = l.split()
        if r:
            fs = frozenset(first(r).split(', '))
        else:
            fs = frozenset()
        return cls(name, eval(weight), fs)

    def calc_total_weight(self, data):
        weights = {c: data[c].calc_total_weight(data) for c in self.children}
        if len(set(weights.values())) > 1:
            determine_culprit(data, weights)
        return self.weight + sum(weights.values())


def determine_culprit(data, weights):
    c = Counter(weights.values())
    correct, incorrect = map(itemgetter(0), c.most_common(2))
    adjustment = correct - incorrect
    for name, weight in weights.items():
        if weight == incorrect:
            raise ResultException(data[name].weight + adjustment)


def parse_data():
    return {pi.name: pi for pi in map(ProgInfo.from_str, U.read_file(7, 2017))}


def aoc07_a(data):
    """find bottom"""
    non_head_names = set(chain.from_iterable(map(attrgetter('children'), data.values())))
    return first(data.keys() - non_head_names)


def aoc07_b(data, start):
    try:
        data[start].calc_total_weight(data)
    except ResultException as e:
        return first(e.args)


def __main():
    data = parse_data()
    head = aoc07_a(data)
    print(head)
    print(aoc07_b(data, head))


if __name__ == '__main__':
    __main()
