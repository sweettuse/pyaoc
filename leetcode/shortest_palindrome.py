__author__ = 'acushner'

# https://leetcode.com/problems/shortest-palindrome/
from itertools import chain, groupby

from pyaoc2019.utils import timer


def _compress(s):
    return [(char, sum(1 for _ in group)) for char, group in groupby(s)]


def _expand(l):
    return ''.join(c * n for c, n in l)
    pass


def _get_prefix(s):
    l, r = 0, len(s) - 1
    to_add = []
    while l < r:
        c1, n1 = s[l]
        c2, n2 = s[r]
        if c1 == c2 and n2 >= n1:
            to_add.append((c1, n2 - n1))
            l += 1
        else:
            to_add.append((c2, n2))
        r -= 1
    if to_add:
        to_add.append(s[l])
    return _expand(to_add)


def shortest_palindrome(s):
    s = _compress(s)
    prefix = _get_prefix(s)
    print(prefix, s)
    return ''.join(chain(reversed(prefix), _expand(s)))


@timer
def __main():
    num_as = 2
    s = num_as * 'a' + 'cd' + num_as * 'a'
    print(s)
    print(shortest_palindrome(s))


if __name__ == '__main__':
    __main()
