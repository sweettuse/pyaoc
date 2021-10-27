__author__ = 'acushner'

# https://leetcode.com/problems/frog-jump/
from functools import lru_cache


def can_cross(stones) -> bool:
    target = stones[-1]
    stones = set(stones)

    @lru_cache(None)
    def _can_cross(pos, jump_size):
        if pos == target:
            return True

        if pos > target or pos < 0 or jump_size <= 0 or pos not in stones:
            return False

        for offset in (1, 0, -1):
            new_jump_size = jump_size + offset
            new_pos = pos + new_jump_size
            if new_pos in stones and _can_cross(new_pos, new_jump_size):
                return True

        return False

    return _can_cross(1, 1)


def __main():
    import sys
    sys.setrecursionlimit(10000)
    stones = [0, 1, 3, 5, 6, 8, 12, 17]
    stones = list(range(1000))
    # stones = [0, 1, 2, 3, 4, 8, 9, 11]
    # stones = [0, 2]
    print(can_cross(stones))

    pass


if __name__ == '__main__':
    __main()
