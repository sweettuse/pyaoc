import os
import pickle
import sys
import time
from collections import deque
from contextlib import contextmanager
from enum import Enum
from functools import wraps
from itertools import islice
from pathlib import Path

__author__ = 'acushner'

from typing import Any, Generator, Iterable, NamedTuple, Callable, TypeVar

T = TypeVar('T')

from pyaoc2019.colors.tile_utils import RC

mapt = lambda fn, *args: tuple(map(fn, *args))

def get_file_path(name, *, depth=1):
    p, _ = os.path.split(sys._getframe(depth).f_globals['__file__'])
    # path = Path(f'/Users/acushner/software/pyaoc/pyaoc{year}/inputs')
    if isinstance(name, int):
        name = f'{name:02d}'
    return Path(f'{p}/inputs') / name


def read_file(name, year=2019, *, do_strip=True):
    path = get_file_path(name, depth=2)
    with open(path) as f:
        res = f.readlines()
    if do_strip:
        res = list(map(str.strip, res))
    return res


@contextmanager
def localtimer():
    start = time.perf_counter()
    yield
    print('func took', time.perf_counter() - start)


def timer(func):
    total = 0
    ncalls = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal total, ncalls
        ncalls += 1
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            total += time.perf_counter() - start
            print(
                f'{func.__name__!r} took {(time.perf_counter() - start):.6f} seconds, '
                f'{ncalls=} for {total:.3f} seconds'
            )

    return wrapper


def chunks(it: Iterable[T], size: int) -> Generator[list[T], None, None]:
    it = iter(it)
    yield from iter(lambda: list(islice(it, size)), [])


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


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Coord(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Coord(-self.x, -self.y)

    def __mul__(self, other):
        return Coord(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return self - other

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def hex_manhattan(self):
        if sign(self.x) == sign(self.y):
            return abs(self.x + self.y)
        return max(abs(self.x), abs(self.y))

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

    def __neg__(self):
        return self.rotated(0).rotated(0)


def exhaust(iterable_or_fn, *args):
    if args:
        iterable_or_fn = map(iterable_or_fn, *args)
    deque(iterable_or_fn, maxlen=0)


class SliceableDeque(deque):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._get_slice(item)
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            return self._set_slice(key, value)
        return super().__setitem__(key, value)

    def _get_slice(self, item: slice):
        return type(self)(islice(self, item.start, item.stop, item.step))

    def _set_slice(self, key: slice, value):
        vals = self[key]
        offset = key.start or 0
        self.rotate(-offset)
        for _ in range(len(vals)):
            self.popleft()
        self.extendleft(reversed(value))
        self.rotate(offset)


class Pickle:
    _outdir = Path('/tmp/.pydata')

    @classmethod
    def read(cls, *filenames):
        res = []
        for n in filenames:
            with open(cls._outdir / n, 'rb') as f:
                res.append(pickle.load(f))
        if len(res) == 1:
            res = res.pop()
        return res

    @classmethod
    def write(cls, **name_obj_pairs):
        os.makedirs(cls._outdir, exist_ok=True)
        for n, obj in name_obj_pairs.items():
            with open(cls._outdir / n, 'wb') as f:
                pickle.dump(obj, f)


def identity(x):
    return x
