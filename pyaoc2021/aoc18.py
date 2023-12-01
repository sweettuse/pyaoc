from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from math import floor, ceil
from typing import Literal, NamedTuple, Iterable, Optional, TypeGuard

from pyaoc2019.utils import read_file, mapt, timer

__author__ = 'acushner'


def parse_data(*, debug=False) -> tuple[Pair, ...]:
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = read_file(filename, 2021)
    return mapt(Pair.from_str, data)


@dataclass(repr=False)
class Pair:
    l: int | Pair
    r: int | Pair
    parent: tuple[Pair, int | str] | None = None

    def __add__(self, other):
        return Pair(self, other)

    @classmethod
    def from_str(cls, s):
        s = s.replace('[', 'Pair(')
        s = s.replace(']', ')')
        res = eval(s)
        res.set_parents()
        return res

    @classmethod
    def from_strs(cls, strs):
        pairs = map(cls.from_str, strs)
        return [p.reduce() for p in pairs]

    def set_parents(self):
        for p in self:
            if is_pair(p.l):
                p.l.parent = p, 'l'
            if is_pair(p.r):
                p.r.parent = p, 'r'

    def __iter__(self):
        yield self
        if is_pair(self.l):
            yield from self.l
        if is_pair(self.r):
            yield from self.r

    @property
    def is_regular(self):
        return isinstance(self.l, int) and isinstance(self.r, int)

    @property
    def magnitude(self) -> int:
        l = self.l if is_int(self.l) else self.l.magnitude
        r = self.r if is_int(self.r) else self.r.magnitude
        return 3 * l + 2 * r

    @property
    def list_str(self) -> str:
        res = []

        def _recurse(p):
            res.append('[')
            if is_pair(p.l):
                _recurse(p.l)
            else:
                res.append(str(p.l))
            res.append(',')
            if is_pair(p.r):
                _recurse(p.r)
            else:
                res.append(str(p.r))
            res.append(']')

        _recurse(self)
        return ''.join(res)

    def __repr__(self):
        return self.list_str

    __str__ = __repr__

    def reduce(self):
        while True:
            self.set_parents()
            if check_explode(self):
                continue
            if check_split(self):
                continue
            break
        return self


class DPS(NamedTuple):
    depth: int
    pair: Pair
    side: str

    def __repr__(self):
        if self.side == 'lr':
            p_str = f'Pair{self.pair.l, self.pair.r}'
        elif self.side == 'l':
            p_str = f'Pair({self.pair.l}, _)'
        else:
            p_str = f'Pair(_, {self.pair.r})'

        return f'DPS(depth={self.depth}, {p_str})'


def is_pair(p) -> TypeGuard[Pair]:
    return isinstance(p, Pair)


def is_int(p) -> TypeGuard[int]:
    return isinstance(p, int)


def traverse(pair: Pair, depth=0) -> Iterable[DPS]:
    """yield pair information for regular numbers"""
    if pair.is_regular:
        yield DPS(depth, pair, 'lr')
    else:
        if is_pair(pair.l):
            yield from traverse(pair.l, depth + 1)
        else:
            yield DPS(depth, pair, 'l')

        if is_pair(pair.r):
            yield from traverse(pair.r, depth + 1)
        else:
            yield DPS(depth, pair, 'r')


def check_explode(pair: Pair) -> bool:
    last_seen_reg = None
    to_explode = None
    next_reg = None
    state = 'check_explode'
    for dps in traverse(pair):
        if state == 'check_explode':
            if dps.side == 'lr' and dps.depth >= 4:
                to_explode = dps
                state = 'find_next'
                continue
            else:
                last_seen_reg = dps
        elif state == 'find_next':
            next_reg = dps
            break

    def _inc(dsp, v, default):
        side = default if dsp.side == 'lr' else dsp.side
        cur = getattr(dsp.pair, side)
        setattr(dsp.pair, side, v + cur)

    if to_explode:
        if last_seen_reg:
            _inc(last_seen_reg, to_explode.pair.l, 'r')
        if next_reg:
            _inc(next_reg, to_explode.pair.r, 'l')
        setattr(*to_explode.pair.parent, 0)
        return True

    return False


def check_split(pair: Pair) -> Optional[Literal[True]]:
    for dps in traverse(pair):
        for side in dps.side:
            if (v := getattr(dps.pair, side)) >= 10:
                half = v / 2
                l, r = floor(half), ceil(half)
                setattr(dps.pair, side, Pair(l, r))
                return True


def run(pair_str: str):
    pair = Pair.from_str(pair_str)
    return pair.reduce()


def _test():
    assert run('[[[[[9,8],1],2],3],4]').list_str == '[[[[0,9],2],3],4]'
    assert run('[7,[6,[5,[4,[3,2]]]]]').list_str == '[7,[6,[5,[7,0]]]]'
    assert run('[[6,[5,[4,[3,2]]]],1]').list_str == '[[6,[5,[7,0]]],3]'

    assert run('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]').list_str == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'
    strs = '[1,1] [2,2] [3,3] [4,4] [5,5]'.split()
    res = pair_sum(Pair.from_strs(strs))
    assert res.magnitude == 791
    assert Pair.from_str('[[9,1],[1,9]]').magnitude == 129
    test_str = '''
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''
    strs = filter(bool, test_str.splitlines())
    pairs = Pair.from_strs(strs)
    assert pair_sum(pairs).magnitude == 4140


def pair_sum(pairs: Iterable[Pair]):
    pairs = iter(pairs)
    cur = next(pairs)
    cur.reduce()
    for p in pairs:
        p.reduce()
        cur = cur + p
        cur.reduce()

    return cur


@timer
def part1(pairs):
    return pair_sum(pairs).magnitude


@timer
def part2(pairs):
    max_mag = -float('inf')
    for p1, p2 in product(pairs, repeat=2):
        if p1 is p2:
            continue
        l1, r1 = deepcopy(p1), deepcopy(p2)
        max_mag = max(max_mag, (l1 + r1).reduce().magnitude)
    return max_mag


def __main():
    _test()
    debug = False
    print(part1(parse_data(debug=debug)))
    print(part2(parse_data(debug=debug)))


if __name__ == '__main__':
    __main()
