from collections import defaultdict
from functools import reduce
from operator import itemgetter

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

data = read_file('07.test', 2020)
data = read_file('07.test2', 2020)
data = read_file(7, 2020)


def parse_line(l):
    def parse_inner(i: str):
        num, color = i.split(' ', maxsplit=1)
        return int(num), color

    l = l.replace('.', '').replace('bags', 'bag').strip()
    outer, inner = l.split(' contain ')

    if 'no other bag' in inner:
        return outer, []

    inner = inner.split(', ')
    return outer, list(map(parse_inner, inner))


data = [parse_line(l) for l in data]


def part1():
    child_parent_map = defaultdict(set)
    for parent, children in data:
        for c in map(itemgetter(1), children):
            child_parent_map[c].add(parent)

    def _get_parents(color='shiny gold bag'):
        if (parents := child_parent_map.get(color)) is None:
            return set()
        return reduce(set.union, (parents, *(_get_parents(r) for r in parents)))

    return len(_get_parents())


def part2():
    parent_children_map = dict(data)

    def _get_num_bags(color='shiny gold bag'):
        if not (children := parent_children_map.get(color)):
            return 0
        return sum(n * (_get_num_bags(child_color) + 1) for n, child_color in children)

    return _get_num_bags()


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
