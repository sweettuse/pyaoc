from typing import List, Set, Dict

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


def parse_data(rows: List[str]):
    def _parse_row(row):
        source, targets = row.split('<->')
        return int(source), set(eval(targets + ','))

    return dict(map(_parse_row, rows))


def get_connected(data: Dict[int, Set[int]], start: int) -> Set[int]:
    """do it, bro!"""
    seen = set()
    stack = [{start}]
    while stack:
        current = stack.pop()
        seen.update(current)
        stack.extend(to_check for c in current if (to_check := data[c] - seen))
    return seen


def get_connected_r(data: Dict[int, Set[int]], start: int) -> Set[int]:
    seen = set()

    def _helper(cur: int):
        if to_check := data[cur] - seen:
            seen.update(to_check)
            return to_check.union(*map(_helper, to_check))
        return set()

    return _helper(start)


def aoc12_a(data):
    return len(get_connected(data, 0))


def get_num_distinct_groups(data):
    res = set()
    all_progs = set(data)
    num_groups = 0
    while remaining := all_progs - res:
        num_groups += 1
        res |= get_connected(data, first(remaining))
    return num_groups


def __main():
    data = parse_data(U.read_file(12, 2017))
    with U.localtimer():
        print(aoc12_a(data))
        print(get_num_distinct_groups(data))


if __name__ == '__main__':
    __main()
