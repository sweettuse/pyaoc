__author__ = 'acushner'

# 8.13 Stack of Boxes: You have a stack of n boxes, with widths wi, heights hi, and depths di. The boxes
# cannot be rotated and can only be stacked on top of one another if each box in the stack is strictly
# larger than the box above it in width, height, and depth. Implement a method to compute the
# height of the tallest possible stack. The height of a stack is the sum of the heights of each box.
# Hints:#755, #194, #274, #260, #322, #368, #378
from functools import lru_cache
from math import prod
from typing import NamedTuple

from pyaoc2019.utils import timer


class Box(NamedTuple):
    w: int
    h: int
    d: int

    def strictly_gt(self, other):
        return self.w > other.w and self.h > other.h and self.d > other.d


@timer
def max_height(boxes: list[Box]):
    if not boxes:
        return 0

    boxes = sorted(boxes)

    @lru_cache(None)
    def _max_height(idx):
        if idx >= len(boxes):
            return 0

        cur = boxes[idx]

        if idx == 0:
            return cur.h

        max_stack = 0
        for i in range(idx - 1, -1, -1):
            if cur.strictly_gt(boxes[i]):
                max_stack = max(max_stack, _max_height(i))
        return cur.h + max_stack

    return max(_max_height(i) for i in range(len(boxes)))


def __main():
    boxes = [Box(1, 2, 7), Box(4, 1, 6), Box(7, 8, 9)] * 2000
    print(prod(boxes[1]))
    print(max_height(boxes))
    # print(boxes[1] > boxes[2])
    pass


if __name__ == '__main__':
    __main()
