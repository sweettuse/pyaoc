import pickle
import time
from collections import deque
from contextlib import contextmanager
from enum import Enum
from functools import wraps
from itertools import islice
from pathlib import Path

__author__ = 'acushner'

from typing import Any, Iterable, NamedTuple

from pyaoc2019.colors.tile_utils import RC


def read_file(name, year=2019):
    path = Path(f'/Users/acushner/software/pyaoc2019/pyaoc{year}/inputs')
    if isinstance(name, int):
        name = f'{name:02d}'
    with open(path / name) as f:
        return list(map(str.strip, f.readlines()))


@contextmanager
def localtimer():
    start = time.perf_counter()
    yield
    print('func took', time.perf_counter() - start)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f'{func.__name__!r} took {time.perf_counter() - start} seconds')

    return wrapper


def chunks(it: Iterable[Any], size):
    it = iter(it)
    yield from iter(lambda: list(islice(it, size)), [])


def __main():
    pass


if __name__ == '__main__':
    __main()


class Atom:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, val):
        self._val = val

    def __str__(self):
        return f'Atom({self._val})'

    __repr__ = __str__


class classproperty:
    def __init__(self, f):
        self._get = f
        self._set = None

    def __get__(self, instance, cls):
        return self._get(cls)

    def setter(self, f):
        self._set = f
        return self

    def __set__(self, instance, value):
        if not self._set:
            raise AttributeError(f"can't set attribute {self._get.__name__}")
        self._set(type(instance), value)


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Coord(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Coord(-self.x, -self.y)

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def rc(self):
        return RC(self.y, self.x)


class Direction(Enum):
    up = Coord(1, 0)
    right = Coord(0, 1)
    down = Coord(-1, 0)
    left = Coord(0, -1)

    def rotated(self, val):
        """
        0: rotate 90 deg counter-clockwise
        1: rotate 90 deg clockwise
        """
        dirs = list(Direction)
        val = 2 * val - 1
        new_idx = (dirs.index(self) + val) % len(dirs)
        return dirs[new_idx]


def exhaust(iterable):
    deque(iterable, maxlen=0)


class Pickle:
    _outdir = Path('/tmp/.pydata')

    @classmethod
    def read(cls, *filenames):
        res = []
        for n in filenames:
            with open(cls._outdir / n, 'rb') as f:
                res.append(pickle.load(f))
        return res

    @classmethod
    def write(cls, **name_obj_pairs):
        for n, obj in name_obj_pairs.items():
            with open(cls._outdir / n, 'rb') as f:
                pickle.dump(obj, f)
