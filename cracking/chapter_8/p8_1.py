__author__ = 'acushner'

# 8.1 Triple Step: A child is running up a staircase with n steps and can hop either 1 step, 2 steps, or 3
# steps at a time. Implement a method to count how many possible ways the child can run up the
# stairs.
from functools import lru_cache
from collections import deque


# issues:
# fucked up starting case
# should've written recursively to start then iteratively

def triple_step(n, size=3):
    nums = deque([1, 1, 2], maxlen=size)
    if n <= 0:
        return 1
    if n < 2:
        return nums[n - 1]

    for _ in range(2, n):
        nums.append(sum(nums))
    return nums[-1]


@lru_cache(None)
def t_step(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return t_step(n - 1) + t_step(n - 2) + t_step(n - 3)


def __main():
    for i in range(10):
        print(i, triple_step(i, 3), '|', t_step(i))
    pass


if __name__ == '__main__':
    __main()
