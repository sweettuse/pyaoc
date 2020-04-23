from typing import Set, Dict

from cytoolz import first

from pyaoc2019.utils import read_file

__author__ = 'acushner'

Connections = Dict[int, Set[int]]


def parse_file(fname=12) -> Connections:
    def _parse_row(row):
        source, target = row.split('<->')
        return int(source), set(eval(target + ','))

    return dict(map(_parse_row, read_file(fname, 2017)))


def get_connected(conns: Connections, start: int = 0):
    """do it, bro!"""
    seen = set()
    stack = [{start}]
    while stack:
        cur = stack.pop()
        seen.update(cur)
        stack.extend(to_check for c in cur if (to_check := conns[c] - seen))
    return seen


def f(v, l=[]):
    l.append(v)
    return l


print(f(1))
print(f(2))


def cache(s: str, d={}):
    if s in d:
        return d[s]
    d[s] = s
    return s


"""
snth
snth
snth
snth
snth
snth
snth
snth
snth
snth
"""


def get_connected_r(conns: Connections, start: int = 0):
    seen = set()

    def _helper(val):
        seen.add(val)
        for c in conns[val]:
            if c not in seen:
                _helper(c)

    _helper(start)
    return seen


def aoc12_a(conns: Connections):
    return len(get_connected_r(conns))


def aoc12_b(conns: Connections):
    all_progs = set(conns)
    seen = set()
    total_groups = 0
    while remaining := all_progs - seen:
        seen |= get_connected(conns, first(remaining))
        total_groups += 1
    return total_groups


def __main():
    conns = parse_file()
    print(aoc12_a(conns))
    print(aoc12_b(conns))


if __name__ == '__main__':
    __main()
