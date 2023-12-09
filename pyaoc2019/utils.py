from __future__ import annotations
import os
import pickle
import re
import sys
import time
from collections import deque
from enum import Enum
from functools import partial, total_ordering, wraps
from itertools import islice
from pathlib import Path

__author__ = "acushner"

from typing import (
    Generator,
    Iterable,
    Iterator,
    NamedTuple,
    Callable,
    Optional,
    TypeVar,
    ParamSpec,
)


T = TypeVar("T")
P = ParamSpec("P")


def mapt(fn: Callable[..., T], *a) -> tuple[T, ...]:
    return tuple(map(fn, *a))

def mapl(fn: Callable[..., T], *a) -> list[T]:
    return list(map(fn, *a))

def read_file(name, year=2019, *, do_strip=True, do_split=True) -> str | list[str]:
    """note, year no longer used - now parsed by frame hacking"""
    path = get_file_path(name, depth=2)
    with open(path) as f:
        if do_split:
            res = f.readlines()
        else:
            return f.read()
    if do_strip:
        res = list(map(str.strip, res))
    return res


def get_file_path(name, *, depth=1):
    p, _ = os.path.split(sys._getframe(depth).f_globals["__file__"])
    # path = Path(f'/Users/acushner/software/pyaoc/pyaoc{year}/inputs')
    if isinstance(name, int):
        name = f"{name:02d}"
    return Path(f"{p}/inputs") / name


def get_all_ints(s: str) -> Iterator[int]:
    """parse all ints from a string"""
    return map(int, re.findall("[-]?\d+", s))


class localtimer:
    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc, tb):
        print("func took", time.perf_counter() - self.start)


def timer(func: Optional[Callable[P, T]] = None, *, n_times: int = 1) -> Callable[P, T]:
    total = 0
    ncalls = 0

    if not func:
        return partial(timer, n_times=n_times)

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal total, ncalls
        ncalls += 1
        start = time.perf_counter()
        try:
            res = func(*args, **kwargs)
            if n_times > 1:
                for _ in range(n_times - 1):
                    func(*args, **kwargs)
            return res
        finally:
            total += time.perf_counter() - start
            print(
                f"{func.__name__!r} took {(time.perf_counter() - start):.6f} seconds, "
                f"{ncalls=} for {total:.3f} seconds"
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
        return f"Atom({self._val})"

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


@total_ordering
class RC(NamedTuple):
    """represent row/column coords"""

    r: int
    c: int

    def to(self, other):
        """range from self to other"""
        yield from (
            RC(r, c) for r in range(self.r, other.r) for c in range(self.c, other.c)
        )

    def in_bounds(self, rc_ul, rc_lr) -> bool:
        """return True if self inside the bounds of [upper_left, lower_right)"""
        return not (
            self[0] < rc_ul[0]
            or self[1] < rc_ul[1]
            or self[0] >= rc_lr[0]
            or self[1] >= rc_lr[1]
        )

    @property
    def area(self):
        return self.r * self.c

    def __add__(self, other) -> RC:
        return type(self)(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other) -> RC:
        return type(self)(self[0] - other[0], self[1] - other[1])

    def __mul__(self, n: int):
        return type(self)(self[0] * n, self[1] * n)

    def __floordiv__(self, other) -> RC:
        return type(self)(self[0] // other[0], self[1] // other[1])

    def __mod__(self, other) -> RC:
        return type(self)(self[0] % other[0], self[1] % other[1])

    def __lt__(self, other):
        return self[0] < other[0] and self[1] < other[1]

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]

    def __rmod__(self, other) -> RC:
        return self % other

    def __divmod__(self, other) -> tuple[RC, RC]:
        return self // other, self % other

    def __neg__(self):
        return type(self)(-self[0], -self[1])

    @property
    def manhattan(self):
        return abs(self.r) + abs(self.c)


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return type(self)(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return type(self)(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __mul__(self, other):
        return type(self)(self.x * other, self.y * other)

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
    _outdir = Path("/tmp/.pydata")

    @classmethod
    def read(cls, *filenames):
        res = []
        for n in filenames:
            with open(cls._outdir / n, "rb") as f:
                res.append(pickle.load(f))
        if len(res) == 1:
            res = res.pop()
        return res

    @classmethod
    def write(cls, **name_obj_pairs):
        os.makedirs(cls._outdir, exist_ok=True)
        for n, obj in name_obj_pairs.items():
            with open(cls._outdir / n, "wb") as f:
                pickle.dump(obj, f)


def identity(x):
    return x


def take(n, iterable):
    return list(islice(iterable, n))


class PutIter:
    """iterator that you can put back values to

    basically allows `peek`
    """

    def __init__(self, iterable):
        self.it = iter(iterable)
        self._buffer = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self._buffer:
            return self._buffer.pop()
        return next(self.it)

    def put(self, value):
        self._buffer.appendleft(value)
