from functools import lru_cache, wraps

from more_itertools import first

from pyaoc2017.aoc16_st import Dance, STARTING_LAYOUT
from pyaoc2019.utils import read_file, localtimer

__author__ = 'acushner'


def run(n_times=1, starting_layout=STARTING_LAYOUT):
    """memoized solution for 16

    of interest: a hand-rolled cache decorator is about 40% slower than lru_cache,
    i assume because lru_cache is implemented in C
    """
    insts = first(read_file(16, 2017)).split(',')
    print(insts)
    sl = starting_layout
    d = Dance(sl)

    @lru_cache(maxsize=None)
    def helper(_: str) -> str:
        d.run(insts)
        return ''.join(d.layout)

    for _ in range(n_times):
        sl = helper(sl)
    return sl


def __main():
    with localtimer():
        print(run(int(1e9)))


if __name__ == '__main__':
    __main()
