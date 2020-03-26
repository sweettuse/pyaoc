from collections import defaultdict
from typing import NamedTuple, List, Set, Dict
from pyaoc2019.colors.tile_utils import RC

import pyaoc2019.utils  as U

__author__ = 'acushner'


class Claim(NamedTuple):
    """#965 @ 322,681: 19x24"""
    id: int
    ul: RC
    shape: RC

    @classmethod
    def from_str(cls, s):
        cid, _, ul, shape = s.split()
        cid = int(cid[1:])

        c, r = map(int, ul[:-1].split(','))
        ul = RC(r, c)

        c, r = map(int, shape.split('x'))
        return cls(cid, ul, RC(r, c))

    @property
    def covered_positions(self):
        return [rc for rc in self.ul.to(self.ul + self.shape)]


RCClaimMap = Dict[RC, Set[Claim]]


def _gen_rc_claim_map(data: List[Claim]) -> RCClaimMap:
    res = defaultdict(set)
    for c in data:
        for rc in c.covered_positions:
            res[rc].add(c)
    return res


def aoc03_a(rc_claim_map: RCClaimMap):
    return sum(len(s) > 1 for s in rc_claim_map.values())


def aoc03_b(data: List[Claim], rc_claim_map: RCClaimMap):
    all_ids = {c.id for c in data}
    overlaps = {c.id
                for s in rc_claim_map.values() if len(s) > 1
                for c in s}
    return (all_ids - overlaps).pop()


def __main():
    data = list(map(Claim.from_str, U.read_file(3, 2018)))
    rc_claim_map = _gen_rc_claim_map(data)
    print(aoc03_a(rc_claim_map))
    print(aoc03_b(data, rc_claim_map))


if __name__ == '__main__':
    __main()
