from typing import List, Set, Dict

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


def parse_data(rows: List[str]):
    res = {}
    for r in rows:
        source, targets = r.split('<->')
        res[int(source)] = set(eval(targets + ','))
    return res


def get_connected(data: Dict[int, Set[int]], start: int) -> Set[int]:
    stack = [{start}]
    res = set()
    while stack:
        current = stack.pop()
        res.update(current)
        stack.extend(to_check for c in current if (to_check := data[c] - res))
    return res


def aoc12_a(data):
    return len(get_connected(data, 0))


def get_num_distinct_groups(data):
    res = set()
    total_progs = set(data)
    total_groups = 0
    while remaining := total_progs - res:
        total_groups += 1
        res |= get_connected(data, first(remaining))
    return total_groups


def __main():
    data = parse_data(U.read_file(12, 2017))
    print(aoc12_a(data))
    print(get_num_distinct_groups(data))


if __name__ == '__main__':
    __main()
