from collections import defaultdict
from itertools import product

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = read_file(filename, 2015)
    num_rows, num_cols = len(data), len(data[0])
    return num_rows, num_cols, {(r, c)
                                for r, row in enumerate(data)
                                for c, v in enumerate(row)
                                if v == '#'}


offsets = set(product(range(-1, 2), repeat=2)) - {(0, 0)}


def _inc(num_r, num_c, on):
    def _is_valid(r, c):
        return 0 <= r < num_r and 0 <= c < num_c

    counts = defaultdict(int)
    for r, c in on:
        for r_off, c_off in offsets:
            if _is_valid(new_r := r + r_off, new_c := c + c_off):
                counts[new_r, new_c] += 1

    threes = {rc for rc, c in counts.items() if c == 3}
    twos = {rc for rc, c in counts.items() if c == 2}
    off_to_on = threes - on
    on_to_on = on & (threes | twos)
    return off_to_on | on_to_on


def parts1and2(num_r, num_c, on, always_on=frozenset()):
    on |= always_on
    for _ in range(100):
        on = _inc(num_r, num_c, on) | always_on
    return len(on)


def __main():
    data = parse_data(debug=False)
    print(data)
    print(parts1and2(*data))
    always_on = frozenset({(0, 0), (99, 99), (0, 99), (99, 0)})
    print(parts1and2(*data, always_on))


if __name__ == '__main__':
    __main()
