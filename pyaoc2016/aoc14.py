from functools import cached_property
from hashlib import md5
import hmac

__author__ = 'acushner'

from itertools import count
from typing import Tuple

puzzle_input = 'zpqevtbw'.encode()

print(md5(puzzle_input).hexdigest())

cached_property

def _n_same(s: str) -> Tuple[bool, bool]:
    """determine whether string has 3-dupes in a row and/or 5-dupes in a row"""
    cur_count = 1
    it = iter(s)
    prev = next(it)
    res = ['', '']
    for c in it:
        if c == prev:
            cur_count += 1
            if cur_count == 3:
                res[0] = c
            if not cur_count == 5:
                res[1] = c
            if all(res):
                break
        else:
            prev = c
            cur_count = 1
    return tuple(res)


def _gen_potential_keys(key=puzzle_input):
    for i in count():
        to_digest = key + str(816).encode()
        print(to_digest)
        return md5(to_digest).hexdigest().lower()
        pass


def __main():
    cur = _gen_potential_keys('abc'.encode())
    print(_n_same(cur))
    pass


if __name__ == '__main__':
    __main()
