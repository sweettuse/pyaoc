from collections import defaultdict
from copy import deepcopy

from pyaoc2019.utils import read_file, mapt, exhaust, timer
from typing import NamedTuple, Optional

__author__ = 'acushner'


def parse_data(*, debug=False, data_override=None):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = data_override or read_file(filename, 2021)
    res = defaultdict(set)
    for s in data:
        a, b = s.split('-')
        res[a].add(b)
        res[b].add(a)
    return res


@timer
def part1(graph):
    def _traverse(node: str = 'start', seen: frozenset[str] = frozenset()):
        if node == 'end':
            return 1
        if node.islower():
            if node in seen:
                return 0
            seen |= {node}
        return sum(_traverse(n, seen) for n in graph[node])

    return _traverse()


@timer
def part2(graph):
    valid_paths = set()

    def _traverse(node: str = 'start',
                  seen: frozenset[str] = frozenset(),
                  seen_twice: bool = False,
                  path: tuple[str, ...] = ()) -> None:
        path += (node,)

        if node == 'end':
            valid_paths.add(path)
            return

        if node.islower():
            if node in seen:
                return

            if node != 'start' and not seen_twice:
                exhaust(_traverse(n, seen, seen_twice=True, path=path) for n in graph[node])

            seen |= {node}

        exhaust(_traverse(n, seen, seen_twice, path) for n in graph[node])

    _traverse()
    return len(valid_paths)


@timer
def part2_no_dupes(graph):
    def _traverse(node: str = 'start',
                  seen: frozenset[str] = frozenset({'start'}),
                  seen_twice: bool = False) -> int:

        if node == 'end':
            return 1

        res = 0
        for neighb in graph[node]:
            if neighb.isupper():
                res += _traverse(neighb, seen, seen_twice)
            else:
                if neighb not in seen:
                    res += _traverse(neighb, seen | {neighb}, seen_twice)
                elif not seen_twice and neighb not in {'start', 'end'}:
                    res += _traverse(neighb, seen, True)
        return res

    return _traverse()


def __main():
    # graph = parse_data(debug=False, data_override='start-A\nA-b\nA-end'.splitlines())
    graph = parse_data(debug=False)
    print(part1(graph))
    print(part2(graph))
    print(part2_no_dupes(graph))


if __name__ == '__main__':
    __main()
