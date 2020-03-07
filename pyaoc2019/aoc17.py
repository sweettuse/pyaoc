from typing import List, Set

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.interpreter import Program, parse_file, process, process_no_yield
from pyaoc2019.utils import Coord, Direction

import pyaoc2019.utils as U

__author__ = 'acushner'


class Scaffold(List[List[str]]):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            r, c = key
            return self[r][c]
        return super().__getitem__(key)


class ASCIIComp:
    def __init__(self, program: Program):
        self.program = program
        self.program.suppress_output = True
        self.scaffold = self._get_scaffolding()

    @property
    def scaffold_str(self):
        return '\n'.join(map(''.join, self.scaffold))

    def run(self):
        alignment_coords = self._get_alignment_coords()
        print(alignment_coords)
        return sum(r * c for r, c in alignment_coords)

    def _get_scaffolding(self) -> Scaffold:
        proc = process(self.program)
        lists = map(list, ''.join(map(chr, proc)).splitlines())
        return Scaffold(filter(bool, lists))

    def _get_alignment_coords(self) -> Set[RC]:
        res = set()
        for r_idx, row in enumerate(self.scaffold[1:-1], 1):
            for c_idx, val in enumerate(row[1:-1], 1):
                rc = RC(r_idx, c_idx)
                if self._is_intersection(rc):
                    res.add(rc)

        return res

    def _is_intersection(self, rc: RC):
        return all(self.scaffold[rc + offset] == '#'
                   for offset in (RC(0, 0), RC(-1, 0), RC(1, 0), RC(0, -1), RC(0, 1)))


def aoc11_a():
    ac = ASCIIComp(parse_file(17))
    print(ac.scaffold_str)
    print(ac.run())


def __main():
    aoc11_a()
    pass


if __name__ == '__main__':
    __main()
