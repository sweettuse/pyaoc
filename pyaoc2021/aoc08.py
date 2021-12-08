from collections import defaultdict, Counter
from functools import lru_cache
from itertools import product
from typing import NamedTuple

from more_itertools import first

from pyaoc2019.utils import read_file, mapt, Pickle

__author__ = 'acushner'


class Data(NamedTuple):
    samples: list[str]
    outputs: list[str]

    @classmethod
    def from_str(cls, s):
        samples, outputs = s.split(' | ')
        return cls(samples.split(), outputs.split())


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    fn = int(prob_num)
    if debug:
        fn = f'{prob_num}.test'

    return [Data.from_str(s) for s in read_file(fn, 2021)]


def _len_to_num():
    res = defaultdict(list)
    for n, chars in working.items():
        res[len(chars)].append(n)
    return res


working = dict(zip(range(10), map(set, 'abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg'.split())))
chars_to_num = {frozenset(v): k for k, v in working.items()}
chars = 'abcdefg'
# working_bits = {n: ''.join('1' if c in lit else '0' for c in chars) for n, lit in working.items()}
unique = {n for n, v in _len_to_num().items() if len(v) == 1}


# print([working[v.pop()] for v in _len_to_num().values() if len(v) == 1])


def part1(data):
    return sum(len(v) in unique
               for d in data
               for v in d.outputs)


def _count_chars(words):
    return Counter(c for chars in words for c in chars)


def _unique_len_to_chars(words):
    res = defaultdict(list)
    for chars in words:
        res[len(chars)].append(set(chars))
    return {l: v.pop() for l, v in res.items() if len(v) == 1}


# number of times each letter appears in the the 10 digits with unique frequencies

def _calc_known_freqs():
    res = defaultdict(set)
    for c, n in _count_chars(working.values()).items():
        res[n].add(c)
    return res


known_freqs = _calc_known_freqs()


def _map_by_freq(d: Data) -> dict[str, str]:
    res = {frm: known_freqs[count] for frm, count in _count_chars(d.samples).items()}
    return res


def _find_a(unknown):
    """len(3) -> 7 - len(2) -> 1 - leaves segment 'a' as the only remaining option"""
    return (unknown[3] - unknown[2]).pop()


def _map_by_num(d: Data) -> dict[str, str]:
    known = _unique_len_to_chars(working.values())
    unknown = _unique_len_to_chars(d.samples)
    res = {c: known[n].copy()
           for n in sorted(known, reverse=True)
           for c in unknown[n]}
    res[_find_a(unknown)] = {'a'}
    return res


def _to_int(d: Data, char_map):
    tr = str.maketrans(char_map)
    nums = (chars_to_num[frozenset(o.translate(tr))] for o in d.outputs)
    return int(''.join(map(str, nums)))


def _update(res, other):
    return {c: res[c] & other[c] for c in res}


def _decode(d: Data):
    final = {}
    res = {c: set(chars) for c in chars}
    res = _update(res, _map_by_num(d))
    res = _update(res, _map_by_freq(d))

    while res:
        frm, to = min(res.items(), key=lambda kv: len(kv[1]))
        if not to:
            res.pop(frm)
            continue
        to = to.pop()
        final[frm] = to
        for v in res.values():
            v.discard(to)
    return _to_int(d, final)


def part2(data):
    return sum(map(_decode, data))


def __main():
    data = parse_data(debug=False)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
