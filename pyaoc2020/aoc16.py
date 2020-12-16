from itertools import chain
from math import prod
from typing import NamedTuple, FrozenSet

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

data = read_file(13, 2020)


class Info(NamedTuple):
    desc: str
    valids: FrozenSet[int]

    @classmethod
    def from_str(cls, s: str):
        name, rngs = s.split(': ')
        rngs = rngs.split(' or ')
        res = set()
        for r in rngs:
            start, end = map(int, r.split('-'))
            res |= set(range(start, end + 1))
        return cls(name, res)


def parse_data(fname=16):
    res = [], [], []
    state = 0

    for line in (it := iter(read_file(fname, 2020))):
        if not line:
            state += 1
            next(it)
            continue

        if state == 0:
            res[state].append(Info.from_str(line))
        else:
            res[state].append([int(v) for v in line.split(',')])

    return res


def part1():
    info, _, others = parse_data()
    valids = set.union(*(i.valids for i in info))
    return sum(n for n in chain(*others) if n not in valids)


def part2():
    infos, mine, tix = parse_data()
    mine = mine[0]
    valids = set.union(*(i.valids for i in infos))
    valid_tix = [t for t in tix if set(t) <= valids]

    def _get_possibles():
        """infos idx -> possible ticket field idxs"""
        possibles = {}
        tix_columns = list(map(set, zip(*valid_tix)))

        for i, info in enumerate(infos):
            possibles[i] = {j for j, col in enumerate(tix_columns) if col <= info.valids}

        return possibles

    def _get_info_field_map():
        """infos idx -> ticket field idx"""
        res = {}
        cur = _get_possibles()

        while cur:
            info_row, poss = min(cur.items(), key=lambda kv: len(kv[1]))
            cur.pop(info_row)
            for v in cur.values():
                v -= poss
            res[info_row] = poss.pop()

        return res

    _info_field_map = _get_info_field_map()
    relevant_idxs = [i for i, info in enumerate(infos) if info.desc.startswith('departure')]

    return prod(mine[_info_field_map[idx]] for idx in relevant_idxs)


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
