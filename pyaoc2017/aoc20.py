from collections import deque, defaultdict
from dataclasses import dataclass
from itertools import starmap, count
from typing import List

import pyaoc2019.utils as U

__author__ = 'acushner'


@dataclass(unsafe_hash=True)
class Coord3:
    x: int
    y: int
    z: int

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Particle:
    """p=<1230,-1835,-2016>, v=<171,-267,-285>, a=<-13,16,22>"""
    p: Coord3
    v: Coord3
    a: Coord3
    id: int

    _particle_count = count()

    @classmethod
    def from_str(cls, s):
        fields = s.split(', ')
        return cls(*starmap(Coord3, (eval(f.split('<')[1].replace('>', '')) for f in fields)),
                   next(cls._particle_count))

    def tick(self):
        self.v += self.a
        self.p += self.v

    @staticmethod
    def read_data(fn=20):
        Particle._particle_count = count()
        return [Particle.from_str(p) for p in U.read_file(fn, 2017)]


def aoc20_a(fn=20):
    parts = Particle.read_data(fn)
    key = lambda _p: _p.p.manhattan
    history_len = 500
    history = deque(maxlen=history_len)

    while True:
        U.exhaust(p.tick() for p in parts)
        parts.sort(key=key)
        history.append(parts[0].id)
        if len(history) == history_len and len(set(history)) == 1:
            return parts[0].id


def _find_dupes(parts: List[Particle]):
    by_pos = defaultdict(list)
    for p in parts:
        by_pos[p.p].append(p)

    res = []
    for ps in by_pos.values():
        if len(ps) > 1:
            res.extend(p.id for p in ps)

    return res


def aoc20_b(fn=20):
    parts = Particle.read_data(fn)
    parts_by_id = {p.id: p for p in parts}
    for _ in range(1000):
        U.exhaust(parts_by_id.pop(d) for d in _find_dupes(parts))
        U.exhaust(p.tick() for p in parts)

    return len(parts_by_id)


def __main():
    print(aoc20_a())
    print(aoc20_b())


if __name__ == '__main__':
    __main()
