__author__ = 'acushner'

# 16.17 Contiguous Sequence: You are given an array of integers (both positive and negative). Find the
# contiguous sequence with the largest sum. Return the sum.
# EXAMPLE
# input:2, -8, 3, -2, 4, -10
# Output: 5 ( i. e • , { 3, -2, 4})
# Hints:#530, #552, #566, #593, #613
from itertools import accumulate, combinations


def find_largest_sub(l: list[int]) -> list[int]:
    acc = list(accumulate(l))
    pos_idx = [i for i, v in enumerate(l) if v > 0]
    if not pos_idx:
        return []
    elif len(pos_idx) == 1:
        return [l[pos_idx[0]]]

    mx = float('-inf')
    mx_idxs = None
    for start, end in combinations(pos_idx, 2):
        if (diff := acc[end] - acc[start]) > mx:
            mx = diff
            mx_idxs = start, end

    return l[mx_idxs[0]: mx_idxs[1] + 1]


def find_largest_sub2(l: list[int]) -> list[int]:
    i1, i2 = 0, 0
    running = None
    mx = 0
    start_end = None

    while i1 < len(l) and i2 < len(l):
        # find positive
        # start counting
        # stop when negative
        if running is None:
            if l[i1] <= 0:
                i1 += 1
                continue
            running = l[i1]
            i2 = i1
        else:
            if running > mx:
                mx = running
                start_end = i1, i2
            if running <= 0:
                running = None
                i1 = i2 + 1
                continue

            i2 += 1
            if i2 < len(l):
                running += l[i2]

    return start_end


def find_largest_sub3(l: list[int]) -> list[int]:
    max_sum = cur_sum = 0
    start = end = None
    for i, v in enumerate(l):
        if cur_sum == 0:
            start = i
        cur_sum += v
        if cur_sum > max_sum:
            max_sum = cur_sum
            end = i
        elif cur_sum <= 0:
            cur_sum = 0

    return max_sum, start, end


def __main():
    nums = 2, -8, 3, -2, 4, -10, 1, 2, 3, -16, 50
    # nums = 2, -8, 3, -2, 4, -10
    print(find_largest_sub2(nums))
    print(find_largest_sub3(nums))
    # print(nums[2:5])
    pass


if __name__ == '__main__':
    __main()
