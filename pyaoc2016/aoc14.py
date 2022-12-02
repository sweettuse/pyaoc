from __future__ import annotations
from bisect import bisect_left, bisect_right

from collections import defaultdict
from hashlib import md5
from itertools import count, groupby

from pyaoc2019.utils import exhaust, timer

__author__ = 'acushner'


SALT = 'zpqevtbw'.encode()


class Hashes:
    def __init__(self, salt: bytes = SALT, *, stretch_keys=False):
        self._quint_to_idx: defaultdict[str, list[int]] = defaultdict(list)
        self._idx_to_triples: defaultdict[int, list[str]] = defaultdict(list)
        self._cur_idx = 0
        self._salt = salt
        self._stretch_keys = stretch_keys
        self._add_hashes()

    @timer
    def _add_hashes(self, n=5000):
        for _ in range(n):
            i = self._cur_idx
            h = self.get_md5(i)
            triple_added = False
            for k, vals in groupby(h):
                num_vals = sum(1 for _ in vals)
                if not triple_added and num_vals >= 3:
                    triple_added = True
                    self._idx_to_triples[i].append(k)
                if num_vals >= 5:
                    self._quint_to_idx[k].append(i)

            self._cur_idx += 1

    def get_md5(self, n: int):
        res = md5(self._salt + str(n).encode()).hexdigest()

        if not self._stretch_keys:
            return res

        for _ in range(2016):
            res = md5(res.encode()).hexdigest()

        return res
        

    def valids(self):
        cur = 0
        for idx in count():
            if idx + 4000 >= self._cur_idx:
                self._add_hashes()

            if not (chars := self._idx_to_triples.get(idx)):
                continue

            for c in chars:
                quints = self._quint_to_idx.get(c)
                if not quints:
                    continue

                loc = bisect_right(quints, idx)
                if loc == len(quints):
                    continue
                if idx < (q_idx := quints[loc]) <= idx + 1000:
                    yield cur, idx, q_idx, self.get_md5(idx), self.get_md5(q_idx)
                    cur += 1
                    break

def parts1and2(*, stretch_keys: bool):
    hashes = Hashes(stretch_keys=stretch_keys)
    valids = hashes.valids()
    for _ in range(64):
        res = next(valids)
    return res[1]  # type: ignore

def __main():
    hashes = Hashes('abc'.encode(), stretch_keys=False)
    # hashes = Hashes(stretch_keys=True)
    valids = hashes.valids()
    for _ in range(64):
        print(next(valids))

    print(parts1and2(stretch_keys=False))
    print(parts1and2(stretch_keys=True))


if __name__ == '__main__':
    __main()
