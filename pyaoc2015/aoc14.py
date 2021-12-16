from collections import Counter
from functools import partial

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


class RD(NamedTuple):
    speed: int
    time: int
    rest: int

    @classmethod
    def from_s(cls, s):
        t = s.split()
        return cls(*map(int, (t[3], t[6], t[-2])))

    @property
    def period(self):
        return self.time + self.rest


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return list(map(RD.from_s, read_file(filename, 2015)))


def _dist_after_time(rd: RD, t):
    num_full, rem = divmod(t, rd.period)
    total_s = num_full * rd.time + min(rem, rd.time)
    return total_s * rd.speed


def part1(data):
    dat = partial(_dist_after_time, t=2503)
    return max(map(dat, data))


def _round(data, t):
    res = {rd: _dist_after_time(rd, t) for rd in data}
    best = max(res.values())
    return [rd for rd, v in res.items() if v == best]


def part2(data):
    c = Counter(rd
                for t in range(1, 2504)
                for rd in _round(data, t))
    return max(c.values())


def __main():
    data = parse_data(debug=False)
    print(data)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
