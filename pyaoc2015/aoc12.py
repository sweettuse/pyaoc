import json

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return json.loads(read_file(filename, 2015)[0])


def _is_int(v):
    return isinstance(v, int)


def part1(data, ignore_red=False):
    def _traverse_l(l):
        cur = 0
        for v in l:
            if _is_int(v):
                cur += v
            elif isinstance(v, list):
                cur += _traverse_l(v)
            elif isinstance(v, dict):
                cur += _traverse(v)

        return cur

    def _traverse(d):
        cur = 0
        for k, v in d.items():
            if ignore_red and v == 'red':
                return 0
            if _is_int(k):
                cur += k
            if isinstance(v, dict):
                cur += _traverse(v)
            elif isinstance(v, list):
                cur += _traverse_l(v)
            elif _is_int(v):
                cur += v
        return cur

    return _traverse(data)


def _test():
    assert part1({"a": 2, "b": 4}) == 6
    assert part1(dict(a=[1, {"c": "red", "b": 2}, 3]), True) == 4


def __main():
    data = parse_data(debug=False)
    _test()
    print(part1(data))
    print(part1(data, True))


if __name__ == '__main__':
    __main()
