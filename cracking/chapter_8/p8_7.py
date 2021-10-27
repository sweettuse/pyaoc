__author__ = 'acushner'

# 8.7  Permutations without Dups: Write a method to compute all permutations of a string of unique
# characters.
from functools import lru_cache
from itertools import permutations
from typing import List, Set, Tuple

from pyaoc2019.utils import timer, localtimer


def perms_unique(s: Set[str]) -> List[List[str]]:
    if not s:
        return [[]]

    res = []
    for c in s:
        p = perms_unique(s - {c})
        res.extend([c] + v for v in p)
    return res


def perms_with_dupes(s: str) -> set[str]:
    @lru_cache(None)
    def _perms(s: str):
        if not s:
            return {''}

        res = set()
        for i in range(len(s)):
            res.update(s[i] + v for v in _perms(s[:i] + s[i + 1:]))
        return res

    return _perms(''.join(sorted(s)))


def __main():
    # s = 'abcdefghijklmnop'
    # for i in range(4, 11):
    #     print(s[:i])
    #     with localtimer():
    #         print(len(list(permutations(s[:i]))))
    #     with localtimer():
    #         perms_unique(set(s[:i]))
    #     print(30 * '=')

    s = 'aaabb'
    with localtimer():
        print(len(list(permutations(s))))
    with localtimer():
        print(perms_with_dupes(s))
    print(30 * '=')


if __name__ == '__main__':
    __main()
