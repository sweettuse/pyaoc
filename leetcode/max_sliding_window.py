__author__ = 'acushner'

# https://leetcode.com/problems/sliding-window-maximum/
from collections import deque, defaultdict
from heapq import heapify, heappush, heappop


class MaxHeap:
    def __init__(self, vals):
        self.heap = [-v for v in vals]
        heapify(self.heap)
        self._evicted = defaultdict(int)

    @property
    def max(self):
        while True:
            cur = -self.heap[0]
            if cur not in self._evicted:
                return cur

            heappop(self.heap)
            self._evicted[cur] -= 1
            if not self._evicted[cur]:
                del self._evicted[cur]

    def rm_add(self, to_rm, to_add):
        self._rm(to_rm)
        self._add(to_add)

    def _rm(self, v):
        self._evicted[v] += 1

    def _add(self, v):
        heappush(self.heap, -v)


def max_sliding_window(nums, k):
    if not 0 < k <= len(nums):
        return []

    heap = MaxHeap(nums[:k])
    res = [heap.max]
    for r in range(k, len(nums)):
        heap.rm_add(nums[r - k], nums[r])
        res.append(heap.max)

    return res


def __main():
    # print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
    print(max_sliding_window([1], 1))
    pass


if __name__ == '__main__':
    __main()
