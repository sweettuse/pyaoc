__author__ = 'acushner'

# https://leetcode.com/problems/sum-of-two-integers/
from operator import add

from typing import Tuple, Iterable


class Solution:
    def getSum(self, a: int, b: int) -> int:
        return add(a, b)

    def getSum(self, a: int, b: int) -> int:
        carry = 0
        res = []
        for a, b in zip(*map(to_bits, (a, b))):
            cur, carry = current_bits(a, b, carry)
            res.append(cur)

        return int(''.join(map(str, reversed(res))), 2)


def to_bits(n) -> Iterable[int]:
    neg = n < 0
    s = bin(abs(n))[2:]
    s = s.zfill(32)
    if not neg:
        return map(int, s[::-1])
    res = [int(not v) for v in map(int, s)]
    return reversed(res)
# TODO: handle negative numbers


def current_bits(a, b, carry) -> Tuple[int, int]:
    if a & b:  # both 1
        return carry & a, 1
    if a == b:  # both 0
        return carry, 0
    # else, a == 1, b == 0 or vice versa
    return ~carry & 1, carry


def __main():
    print(list(to_bits(-4)))
    print(current_bits(1, 1, 1))
    print(Solution().getSum(-3, 256))
    pass


if __name__ == '__main__':
    __main()
