from itertools import count

from pyaoc2019.utils import timer

__author__ = 'acushner'

nums = 1, 0, 15, 2, 10, 13


def _play_game(nums=nums):
    spoken = dict(map(reversed, enumerate(nums)))
    prev_num = prev_i = None
    yield from enumerate(nums)
    for i in count(len(nums)):
        res = 0
        if prev_num in spoken:
            res = prev_i - spoken[prev_num]

        spoken[prev_num] = prev_i
        yield res
        prev_i, prev_num = i, res


def part1and2(target_idx=2020):
    for _, res in zip(range(target_idx), _play_game()):
        pass
    return res


@timer
def __main():
    print(part1and2())
    print(part1and2(30000000))


# 211
# 2159626
# '__main' took 11.895331928 seconds


if __name__ == '__main__':
    __main()
