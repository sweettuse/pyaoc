__author__ = 'acushner'

# https://leetcode.com/problems/scramble-string/
from functools import lru_cache
from itertools import product
from random import shuffle


def scramble(s: str) -> set[str]:
    if len(s) == 1:
        return {s}

    res = set()
    for i in range(1, len(s)):
        a, b = s[:i], s[i:]
        a_res = [r for r in scramble(a)]
        b_res = [r for r in scramble(b)]
        res.update(r for s1, s2 in product(a_res, b_res) for r in (s1 + s2, s2 + s1))
    return res


def is_scramble(s1, s2):
    if sorted(s1) != sorted(s2):
        return False

    if len(s1) <= 3:
        return True

    if s1 == s2:
        return True

    @lru_cache(None)
    def _is_scramble(s1, s2):
        print(s1, s2)
        for i in range(1, len(s1)):
            if (_is_scramble(s1[:i], s2[:i]) and _is_scramble(s1[i:], s2[i:])
                    or _is_scramble(s1[:i], s2[-i:]) and _is_scramble(s1[i:], s2[:-i])):
                return True
        return False

    return _is_scramble(s1, s2)


def shitty_scramble(s: str) -> set[str]:
    s = list(s)
    res = set()
    for _ in range(1_000_000):
        shuffle(s)
        res.add(''.join(s))
    return res


def __main():
    s = '12345'
    print(is_scramble('54321', s))
    return
    print(len(scramble(s)))
    print(len(shitty_scramble(s)))
    # print('rgeat' in scramble('great'))
    # for i in range(3, 10):
    #     res = scramble(string.ascii_letters[:i])
    #     print(i, len(res))


if __name__ == '__main__':
    __main()
