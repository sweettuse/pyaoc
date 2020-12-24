from contextlib import suppress
from typing import NamedTuple, FrozenSet, Tuple, Union

from cytoolz import memoize

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


class Rule(NamedTuple):
    idx: int
    matches: Union[str, FrozenSet[Tuple[int, ...]]]

    @classmethod
    def from_str(cls, s: str):
        idx, rules = s.split(': ')
        idx = int(idx)
        if '"' in rules:
            return cls(idx, rules.replace('"', ''))
        rules = rules.split(' | ')
        return cls(idx, frozenset(tuple(map(int, v.split())) for v in rules))


def parse_data(fname='19.test'):
    rules, inputs = res = [], []
    state = 0
    for line in read_file(fname, 2020):
        if line:
            res[state].append(line)
        else:
            state += 1

    rules = map(Rule.from_str, rules)
    return {r.idx: r for r in rules}, inputs


def part1(rules, strs):
    def _is_valid(r: Rule, s: str, offset: int):
        for pattern in r.matches:
            if isinstance(pattern, str):
                return s[offset] == pattern, offset + 1

            total_offset = offset
            valid = True
            for p in pattern:
                cur_valid, total_offset = _is_valid(rules[p], s, total_offset)
                valid &= cur_valid
                if not valid:
                    break

            if valid:
                break

        return valid, total_offset

    r = rules[0]
    total = 0
    for s in strs:
        valid, length = False, None
        with suppress(IndexError):
            valid, length = _is_valid(r, s, 0)
        valid &= (len(s) == length)
        total += bool(valid)
    return total


# ======================================================================================================================

def part2(rules, strs):
    rules = rules.copy()
    max_len = max(map(len, strs))
    for idx in 8, 11:
        rules[idx] = _create_expanded_rule(idx, max_len)

    def _process_all(pattern, offset):
        p, *rest = pattern
        for cur_valid, cur_offset in _is_valid(rules[p], s, offset):
            if cur_valid:
                if not rest:
                    yield cur_valid, cur_offset
                else:
                    yield from _process_all(rest, cur_offset)

    def _is_valid(r: Rule, s: str, offset: int):
        """holy crap, using suppress(IndexError) instead of try/except adds 9 seconds! (23 -> 32)"""
        for pattern in sorted(r.matches, key=len):
            if isinstance(pattern, str):
                if offset < len(s):
                    yield s[offset] == pattern, offset + 1
            else:
                yield from _process_all(pattern, offset)

    r = rules[0]
    total = 0
    for s in strs:
        for valid, length in _is_valid(r, s, 0):
            if valid and len(s) == length:
                total += 1
                break
    return total


def _create_expanded_rule(idx, max_repeats=25) -> Rule:
    final_vals = []
    for i in range(max_repeats):
        if idx == 8:
            final_vals.append((i + 1) * [42])
        else:
            final_vals.append([42] + i * [42] + i * [31] + [31])
    return Rule(idx, frozenset(map(tuple, final_vals)))


@timer
def __main():
    rules, strs = parse_data('19')
    print(part1(rules, strs))
    print(part2(rules, strs))


# 156
# 363
# '__main' took 21.954678905 seconds
# this code is messy, but i don't want to deal with it

if __name__ == '__main__':
    __main()
