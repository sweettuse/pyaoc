__author__ = 'acushner'

# 17.6 Count of 2s: Write a method to count the number of 2s that appear in all the numbers between O
# and n (inclusive).
# EXAMPLE
# Input: 25
# Output: 9 (2, 12, 20, 21, 22, 23, 24 and 25. Note that 22 counts for two 2s.)
# Hints: #573, #6 7 2, #641
from math import log


def count_2s(n):
    """first, for n < 10"""
    res = []

    def _count(first, last):
        print(first, last)
        res.append((first, last))
        if not first:
            return
        return _count(*divmod(first, 10))

    _count(*divmod(n, 10))
    print(res)

    # f, l = res[0]
    # (f + l >= 2) * 1 + (10 *
    # 13 1's
    # 1 * 10 2's + 4 * 1's = >
    #
    # (1 + 5 >= 2) * 2 + (0 + 2 >= 2 +
    # [[(2, 5), (0, 2)]
    # [(1, mult, digit), (10, mult, digit)]
    # num_ones = 1 * (mult + digit >= 2)
    # num_tens = 10 * (mult + digit >= 2) -
    # if digit < 2:
    #    return mult * pos
    # elif digit == 2:
    #    return (mult + 1) * pos - missing
    # else:
    #    return (mult + 1) * pos

    def calc(idx=0):
        pass


def count_2s_crappy(n):
    # total = 0
    # for i in map(str, range(1, n + 1)):
    #     if '2' in i:
    #         print(i, t := i.count('2'))
    #         total += t
    #
    # return total
    return sum(s.count('2') for s in map(str, range(1, n + 1)))


def _get_digits(n):
    div = 10 ** int(log(n, 10))
    res = []
    rem = n
    while div > 0:
        digit, rem = divmod(rem, div)
        res.append((digit, div))
        div //= 10
    return res


def count_2s(n):
    nums = _get_digits(n)
    nums.append((0, 0))
    total = 0
    for (d1, m1), (d2, m2) in zip(nums, nums[1:]):
        if d1 < 2:
            total += m1 / 10
        elif d1 > 2:
            total += m1
        pass


def play():
    # key 10% of numbers are 2
    return _get_digits(40)
    n = 199
    cur_pow = int(log(n, 10))
    digit = n // 10 ** cur_pow
    print(digit)


def __main():
    print(play())
    return
    n = 25
    print(log(999, 10))
    print(count_2s_crappy(n))
    print('========')
    return count_2s(n)
    cur = 10
    for _ in range(6):
        print(cur, count_2s_crappy(cur))
        cur *= 10


if __name__ == '__main__':
    __main()
