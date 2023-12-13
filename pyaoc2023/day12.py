from __future__ import annotations
from dataclasses import dataclass, field
from functools import cache, wraps
from itertools import groupby, product
from operator import attrgetter
import string
from typing import Iterable
from pyaoc2019.utils import exhaust, identity, mapt, mapl, read_file, timer
from rich import print


@dataclass
class Record:
    spring: str
    checksum: list[int]

    @classmethod
    def from_str(cls, s: str) -> Record:
        spring, vals = s.split()
        return cls(spring, mapl(int, vals.split(",")))

    @property
    def num_unknown(self) -> int:
        return self.spring.count("?")

    def num_combinations_simple(self):
        """simple way of literally creating *every* combination and validating it"""
        return sum(map(self._is_valid, self._combinations()))

    def _combinations(self) -> Iterable[str]:
        chars = iter(string.ascii_lowercase)
        base = "".join(c if c != "?" else next(chars) for c in self.spring)
        chars = string.ascii_letters
        maketrans = str.maketrans
        translate = base.translate
        for sub in product("#.", repeat=self.num_unknown):
            yield translate(maketrans(dict(zip(chars, sub))))

    def _is_valid(self, s: str) -> bool:
        counts = [sum(1 for _ in v) for k, v in groupby(s, key="#".__eq__) if k]
        return counts == self.checksum

    @staticmethod
    @cache
    def _split(s: str) -> tuple[str, str]:
        return s[0], s[1:]

    @staticmethod
    @cache
    def _dec_run_counts(run_counts: tuple[int, ...]) -> tuple[int, ...]:
        if not run_counts:
            return ()
        return (run_counts[0] - 1,) + run_counts[1:]

    def num_combinations(self):
        """optimized way"""
        counter = 0

        @cache
        # @_catch_return
        def _helper(spring: str, run_counts: tuple[int, ...], *, in_run: bool = False):
            nonlocal counter
            counter += 1
            if not spring:
                if not run_counts or (len(run_counts) == 1 and run_counts[0] == 0):
                    return 1
                return 0

            if not run_counts:
                return int(set(spring) <= {".", "?"})

            cur, rest = self._split(spring)
            # should end a run
            if run_counts[0] == 0:
                if cur == "#":
                    return 0
                run_counts = run_counts[1:]
                return _helper(rest, run_counts, in_run=False)

            # run_counts and run_counts[0] exist
            # should continue run
            if in_run:
                if cur == ".":
                    return 0
                return _helper(rest, self._dec_run_counts(run_counts), in_run=True)

            # not in run
            res = 0
            if cur in ".?":
                res += _helper(rest, run_counts, in_run=False)
            if cur in "#?":
                res += _helper(rest, self._dec_run_counts(run_counts), in_run=True)
            return res

        res = _helper(self.spring, tuple(self.checksum))
        counts.append(counter)
        cache_infos.append(_helper.cache_info())
        return res

counts = []
cache_infos = []

@dataclass
class Record2(Record):
    @classmethod
    def from_str(cls, s: str) -> Record2:
        tmp = super().from_str(s)
        new_spring = (tmp.spring + "?") * 5
        return cls(new_spring[:-1], 5 * tmp.checksum)


def _catch_return(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        res = fn(*a, **kw)
        print(fn.__name__, *a, kw, 'returned', res)
        return res

    return wrapper


@timer
def part1(fname: str):
    return sum(r.num_combinations() for r in map(Record.from_str, read_file(fname)))


@timer
def part2(fname: str):
    return sum(r.num_combinations() for r in map(Record2.from_str, read_file(fname)))


if __name__ == "__main__":
    print(f'{part1("12.txt")=}')
    print(f'{part2("12.txt")=}')
    print(sorted(counts, reverse=True)[:10])
    print(sum(counts))
    cis = sorted(cache_infos, key=attrgetter('hits'), reverse=True)
    print(cis[:10], cis[-10:])
