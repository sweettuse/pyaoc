import re
from collections import defaultdict

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = iter(read_file(filename, 2015))
    res = defaultdict(set)
    while l := next(data):
        k, v = l.split(' => ')
        res[k].add(v)

    s = next(data)
    return s, dict(res)


def _replace(s, sub, start, end):
    return s[:start] + sub + s[end:]


def part1(s, tr):
    seen = set()
    for target, subs in tr.items():
        for match in re.finditer(target, s):
            for sub in subs:
                seen.add(_replace(s, sub, *match.span()))

    return len(seen)


def part2(s, tr):
    tr = {sub: target
          for target, subs in tr.items()
          for sub in subs}
    tr = dict(sorted(tr.items(), key=lambda kv: -(len(kv[0]) - len(kv[1]))))
    tr = {k.replace('Rn', '(').replace('Ar', ')').replace('Y', ','): v
          for k, v in tr.items()}

    print(tr)


def _test():
    s = 'abcdde'
    tr = dict(dd={'q'})
    print(part1(s, tr))


def __main():
    s, tr = parse_data(debug=False)
    print(len(tr))
    print(tr)
    print(part1(s, tr))
    print(part2(s, tr))


if __name__ == '__main__':
    __main()
