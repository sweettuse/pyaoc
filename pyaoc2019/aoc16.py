import time
from itertools import repeat
import numpy as np
import dask.array as da
import tqdm
from concurrent.futures import ProcessPoolExecutor

from cytoolz import first, take, memoize, comp

import pyaoc2019.utils as U

__author__ = 'acushner'


def parse_file(filename=16) -> str:
    return first(U.read_file(filename))


base_pattern = 0, 1, 0, -1


def coefficients(n):
    pattern = [ind_val for v in base_pattern for ind_val in repeat(v, n)]
    res = (c for coeffs in repeat(pattern) for c in coeffs)
    next(res)
    yield from res


@memoize
def get_coeffs_streams(length: int):
    start = time.time()
    arrays = []
    for i in tqdm.trange(1, length + 1):
        arrays.append(da.from_array(list(take(length, coefficients(i)))))
    res = da.stack(arrays)
    print(time.time() - start)
    return res


mod_abs = comp(lambda a: da.mod(a, 10), np.abs)


def calc_next(str_n: str) -> str:
    ints = da.from_array([int(i) for i in str_n])
    coeffs = get_coeffs_streams(len(str_n))
    return ''.join(map(str, mod_abs((ints * coeffs).sum(1).compute())))


def calc(str_n: str, times: int) -> str:
    for _ in tqdm.trange(times):
        str_n = calc_next(str_n)
    return str_n


def aoc16_a():
    return calc(parse_file(), 100)[:8]


def aoc16_b():
    data = parse_file() * 10000
    offset = int(data[:8])
    res = calc(data, 100)
    return res[offset:offset + 8]


def __main():
    # print(parse_file())
    print(get_coeffs_streams(8)[:5])
    print(calc('12345678', 4))
    print(calc('80871224585914546619083218645595', 100))
    print(aoc16_a())
    print(aoc16_b())


if __name__ == '__main__':
    __main()
