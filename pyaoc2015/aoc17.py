from functools import cache

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = read_file(filename, 2015)
    return 25 if debug else 150, sorted(map(int, data), reverse=True)


def parts1and2(conts, target, max_can_use=float('inf')):
    min_used = float('inf')
    max_used = -min_used

    @cache
    def _num_combs(i=0, rem=target, used=0):
        nonlocal min_used, max_used
        if used >= max_can_use:
            return 0
        if i >= len(conts):
            return 0
        cur_size = conts[i]
        total = 0
        if rem == cur_size:
            total += 1
            min_used = min(min_used, used + 1)
            max_used = max(max_used, used + 1)
        elif rem > cur_size:
            total += _num_combs(i + 1, rem - cur_size, used + 1)
        return total + _num_combs(i + 1, rem, used)

    res = _num_combs()
    return min_used, max_used, res


def __main():
    target, conts = parse_data(debug=False)
    print(conts)
    print(parts1and2(conts, target))
    print(parts1and2(conts, target, 4))


if __name__ == '__main__':
    __main()
