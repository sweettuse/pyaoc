from __future__ import annotations
from collections import Counter, defaultdict
from itertools import chain, combinations, permutations, product
from math import prod
from typing import Iterable, NamedTuple
from more_itertools import first

from rich import print

from pyaoc2019.utils import read_file, mapt

sum_p = lambda v: sum(v, Point3())


class Point3(NamedTuple):
    x: int | float = 0
    y: int | float = 0
    z: int | float = 0

    @classmethod
    def from_str(cls, s) -> Point3:
        return cls(*eval(s))

    def __add__(self, other: Point3 | tuple[int, int, int]) -> Point3:
        return Point3(*((a + b) for a, b in zip(self, other)))

    def __truediv__(self, other: int):
        return Point3(*(v / other for v in self))

    @property
    def center(self) -> Point3:
        return self + Point3(.5, .5, .5)

    @property
    def faces(self) -> frozenset[frozenset[Point3]]:
        res = defaultdict(set)
        for v in self.vertices:
            res[v.x, 0, 0].add(v)
            res[0, v.y, 0].add(v)
            res[0, 0, v.z].add(v)

        return frozenset(map(frozenset, res.values()))

    @property
    def vertices(self) -> tuple[Point3, ...]:
        return tuple(self + o for o in product(range(2), repeat=3))


def parse_data(name):
    return mapt(Point3.from_str, read_file(name))

def _get_exposed_faces(points):
    res = Counter(chain.from_iterable(p.faces for p in points))
    return {p for p, num in res.items() if num == 1}

def part1(name):
    return len(_get_exposed_faces(parse_data(name)))


print(part1(18))

# ==============================================================================
# part 2
# ==============================================================================


def _create_bounding_box(points: list[Point3]) -> tuple[set[Point3], set[Point3]]:
    """return inner unoccupied points and surrounding shell of outer points"""
    min_p = Point3(
        min(x for x, *_ in points),
        min(y for _, y, _ in points),
        min(z for *_, z in points),
    )
    max_p = Point3(
        max(x for x, *_ in points),
        max(y for _, y, _ in points),
        max(z for *_, z in points),
    )
    inner_cube = {
        Point3(*coords)
        for coords in product(
            range(min_p.x, max_p.x + 1),
            range(min_p.y, max_p.y + 1),
            range(min_p.z, max_p.z + 1),
        )
    }

    bounding_cube = {
        Point3(*coords)
        for coords in product(
            range(min_p.x - 1, max_p.x + 2),
            range(min_p.y - 1, max_p.y + 2),
            range(min_p.z - 1, max_p.z + 2),
        )
    }
    return inner_cube - set(points), bounding_cube - inner_cube


offsets = [
    Point3(*v) for v in (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )
]

def _get_surrounded_points(
    points: Iterable[Point3],
    inner_unoccupied: Iterable[Point3],
    outer_shell: Iterable[Point3],
):
    points, inner_unoccupied, outer_shell = map(set, (points, inner_unoccupied, outer_shell))
    seen = set()
    while outer_shell:
        working = [outer_shell.pop()]
        while working:
            cur = working.pop()
            seen.add(cur)
            for o in offsets:
                nxt = cur + o
                if nxt in inner_unoccupied and nxt not in seen:
                    working.append(nxt)
    return inner_unoccupied - seen
    


def part2(name):
    """notes on better approach:

    - cluster all contiguous groups together
    - find all groups that don't contain a voxel that touches the surrounding bounding box
    - remove these faces from the set of exposed faces

    notes on (original) approach:

    - find center of each cube
    - consider only non-contiguous face
    - iterate through each axis to see which faces are "blocked" from that direction
    - hmmm....
    """
    points = parse_data(name)
    inner_unoccupied, outer_shell = _create_bounding_box(points)
    surrounded_points = _get_surrounded_points(points, inner_unoccupied, outer_shell)

    exposed_faces = _get_exposed_faces(points)
    surrounded_faces = set(chain.from_iterable(p.faces for p in surrounded_points))
    return len(exposed_faces - surrounded_faces)

print(part2(18))
