from itertools import count
from typing import NamedTuple

from pyaoc2019.utils import read_file, mapt

__author__ = 'acushner'

# nums = read_file('03.test', 2021)
nums = read_file(3, 2021)

flip = {'1': '0', '0': '1'}


class ZerosOnes(NamedTuple):
    zeros: int
    ones: int

    @classmethod
    def from_tuple(cls, t):
        num_ones = sum(v == '1' for v in t)
        num_zeroes = len(t) - num_ones
        return cls(num_zeroes, num_ones)


def _to_counts(nums=nums) -> list[ZerosOnes]:
    return [ZerosOnes.from_tuple(t) for t in zip(*nums)]


def part1():
    gamma = ['01'[zo.ones > zo.zeros] for zo in _to_counts()]
    gamma_num = int(''.join(gamma), 2)
    epsilon_num = int(''.join(flip[v] for v in gamma), 2)
    return gamma_num * epsilon_num


def _part2_helper(nums, pred):
    nums = nums.copy()
    for i in count():
        counts = _to_counts(nums)
        target = pred(counts[i])
        nums = [n for n in nums if n[i] == target]
        if len(nums) == 1:
            return int(nums[0], 2)


def part2():
    oxygen = _part2_helper(nums, lambda zo: '01'[zo.ones >= zo.zeros])
    co2 = _part2_helper(nums, lambda zo: '10'[zo.ones >= zo.zeros])
    return oxygen * co2


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
