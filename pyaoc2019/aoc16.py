import math
import time
from itertools import repeat
from typing import NamedTuple, List

import dask.array as da
import numpy as np
import tqdm
from cytoolz import first, memoize, comp

import pyaoc2019.utils as U

__author__ = 'acushner'


def parse_file(filename=16) -> str:
    return first(U.read_file(filename))


base_pattern = 0, 1, 0, -1


def coefficients(length, n):
    pattern = [ind_val for v in base_pattern for ind_val in repeat(v, n)]
    res = np.array((math.ceil((length + 1) / len(pattern)) * pattern)[1: length + 1])
    return res


@memoize
@U.timer
def get_coeffs_streams(length: int):
    return np.array([coefficients(length, i) for i in range(1, length + 1)])


mod_abs = comp(lambda a: np.mod(a, 10), np.abs)


def calc_next(str_n: str) -> str:
    ints = np.array([int(i) for i in str_n])
    coeffs = get_coeffs_streams(len(str_n))
    return ''.join(map(str, mod_abs((ints * coeffs).sum(1))))


def calc(str_n: str, times: int) -> str:
    for _ in tqdm.trange(times):
        print(str_n)
        str_n = calc_next(str_n)
    return str_n


# ======================================================================================================================
# DASK
# ======================================================================================================================
mod_abs_dask = comp(lambda a: da.mod(a, 10), np.abs)


@memoize
def get_coeffs_streams_dask(length: int):
    start = time.time()
    arrays = []
    for i in tqdm.trange(1, length + 1):
        arrays.append(da.from_array(coefficients(length, i)))
    res = da.stack(arrays)
    print(time.time() - start)
    return res


def calc_next_dask(str_n: str) -> str:
    ints = da.from_array([int(i) for i in str_n])
    coeffs = get_coeffs_streams(len(str_n))
    print(ints.compute())
    print(coeffs.compute())
    return ''.join(map(str, mod_abs((ints * coeffs).sum(1).compute())))


def calc_dask(str_n: str, times: int) -> str:
    for _ in tqdm.trange(times):
        str_n = calc_next_dask(str_n)
    return str_n


def aoc16_a():
    return calc(parse_file(), 100)[:8]


def aoc16_b():
    data = parse_file() * 10000
    offset = int(data[:8])
    res = calc(data, 100)
    return res[offset:offset + 8]


def powers_of_n(n):
    start = 1
    while True:
        yield start
        start *= n


# ======================================================================================================================
# PART B
# ======================================================================================================================

def chunked_coeffs(length, n):
    pass


class CompressedCoeff(NamedTuple):
    n: int
    val: int


class Coefficients(NamedTuple):
    str_n: str
    n_to_drop: int
    ccs: List[CompressedCoeff]


class AOC16B:
    def __init__(self, str_n: str):
        self.str_n = str_n

    @property
    def str_n(self):
        return self._str_n

    @str_n.setter
    def str_n(self, val: str):
        self._str_n = val
        self._ints = np.array([int(d) for d in val])

    def update(self):
        pass

    @staticmethod
    def _calc_one(ints, index, length):
        pass

    @staticmethod
    def _get_indices(index, length):
        """return indices needed using np.r_ """


# ======================================================================================================================
# MAIN
# ======================================================================================================================
def __main():
    print(calc('00000001', 10))
    # print(calc('80871224585914546619083218645595', 100))
    # print(aoc16_a())

    # print(coefficients(8, 2))

    # for i in take(11, powers_of_n(2)):
    #     print(i, end=', ')
    #     get_coeffs_streams(i)

    # print(get_coeffs_streams(16))
    # print(aoc16_b())


if __name__ == '__main__':
    __main()
