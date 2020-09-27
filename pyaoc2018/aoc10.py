import re
import time
from typing import NamedTuple, List, Tuple

from pyaoc2019.utils import read_file


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)


class Star(NamedTuple):
    pos: Point
    vel: Point

    def move(self, n) -> Point:
        return self.pos + self.vel * n

    @classmethod
    def from_str(cls, s):
        _, p, _, v, _ = re.split('[<>]', s)
        return cls(Point(*eval(p)), Point(*eval(v)))


stars = [Star.from_str(line) for line in read_file(10, 2018)]


def get_bounding_coords(points):
    xs, ys = zip(*points)
    x_min, x_max = min(xs) - 1, max(xs) + 1
    y_min, y_max = min(ys) - 1, max(ys) + 1
    return Point(x_min, y_min), Point(x_max, y_max)


def get_closest_together_stars(stars, n=20000) -> Tuple[List[Point], int]:
    print(len(stars))
    min_area = float('inf')
    res = None
    for i in range(1, n + 1):
        cur_stars = [s.move(i) for s in stars]
        p_min, p_max = get_bounding_coords(cur_stars)
        p = p_max - p_min
        cur_area = p.x * p.y
        if cur_area < min_area:
            res = cur_stars
            min_area = cur_area
        else:
            return res, i - 1


def points_to_str(points):
    p_min, p_max = get_bounding_coords(points)
    array = [[' '] * (p_max.x - p_min.x)
             for _ in range(p_min.y, p_max.y)]

    for p in points:
        array[p.y - p_min.y][p.x - p_min.x] = '#'

    return '\n'.join(''.join(a) for a in array)


def read_message(stars):
    """solve part 1 and 2"""
    start = time.time()
    star_locations, time_elapsed = get_closest_together_stars(stars)
    print(points_to_str(star_locations))
    print()
    print('star time elapsed:', time_elapsed)
    print(time.time() - start)


read_message(stars)