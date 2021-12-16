from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


class Ing(NamedTuple):
    cap: int
    dur: int
    flavor: int
    texture: int
    cals: int

    @classmethod
    def from_str(cls, s):
        t = s.replace(',', '').split()[2:]
        return cls(*map(int, t[::2]))

def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return [Ing.from_str(s) for s in read_file(filename, 2015)]


def part1(data):
    pass


def part2(data):
    pass


def __main():
    data = parse_data(debug=True)
    print(data)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
