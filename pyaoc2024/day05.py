from __future__ import annotations
from collections import defaultdict
from functools import partial
from typing import TypeAlias
from rich import print
from functools import cmp_to_key

from pyaoc2019.utils import read_file


BeforeAfter: TypeAlias = dict[int, set[int]]


def _read_data(*, test=False) -> tuple[BeforeAfter, list[list[int]]]:

    data = read_file("05.txt" if not test else "05.test.txt", do_split=False)
    first, second = data.split("\n\n")

    before_after = defaultdict(set)
    for pair in first.split("\n"):
        before, after = map(int, pair.split("|"))
        before_after[before].add(after)

    updates = [list(eval(row)) for row in second.split("\n")]
    return dict(before_after), updates


def _sort_update(before_after, update: list[int]) -> list[int]:
    def _in_order(l, r):
        if r in before_after.get(l, ()):
            return -1
        return 1

    return sorted(update, key=cmp_to_key(_in_order))


def _is_valid(before_after: BeforeAfter, update) -> bool:
    return update == _sort_update(before_after, update)


def _middle_page(update) -> int:
    return update[len(update) // 2]


def part1(ba: BeforeAfter, updates) -> int:
    sorter = partial(_sort_update, ba)

    return sum(
        _middle_page(upd)
        for upd, s_upd in zip(updates, map(sorter, updates))
        if upd == s_upd
    )


def part2(ba: BeforeAfter, updates) -> int:
    sorter = partial(_sort_update, ba)

    return sum(
        _middle_page(s_upd)
        for upd, s_upd in zip(updates, map(sorter, updates))
        if upd != s_upd
    )


def _main():
    ba, updates = _read_data(test=False)
    print(ba)
    print(part1(ba, updates))
    print(part2(ba, updates))


if __name__ == "__main__":
    _main()
