__author__ = 'acushner'

# 17.4 Missing Number: An array A contains all the integers from Oto n, except for one number which
# is missing. In this problem, we cannot access an entire integer in A with a single operation. The
# elements of A are represented in binary, and the only operation we can use to access them is "fetch
# the jth bit of A[ i ],"which takes constant time. Write code to find the missing integer. Can you do
# it in O(n) time?
# Hints: #670, #659, #683
from functools import reduce, partial
from operator import xor
from random import shuffle


def create_list(n=6):
    nums = list(range(n))
    shuffle(nums)
    nums.remove(2)
    return nums


def _get_ith_bit(n, i):
    return (n >> i) & 1


def __main():
    n = 6
    nums = create_list(n)
    expected = not n & 1

    print(list(map(partial(_get_ith_bit, i=0), nums)))
    assert expected == reduce(xor, map(partial(_get_ith_bit, i=0), nums))
    pass


if __name__ == '__main__':
    __main()
