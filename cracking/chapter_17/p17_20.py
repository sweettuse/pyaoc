__author__ = 'acushner'

# 17.20 Continuous Median: Numbers are randomly generated and passed to a method. Write a program
# to find and maintain the median value as new values are generated.
from heapq import heappush, heappop
from random import randint


class Med:
    def __init__(self, start):
        self.lt = [-start]
        self.gt = []
        self._count = 1

    def add(self, n):
        self._count += 1
        if n <= self.median:
            heappush(self.lt, -n)
        else:
            heappush(self.gt, n)

        if len(self.gt) > len(self.lt):
            heappush(self.lt, -heappop(self.gt))
        elif len(self.lt) > len(self.gt) + 1:
            heappush(self.gt, -heappop(self.lt))

        return self.median

    @property
    def median(self):
        res = -self.lt[0]
        if not self._count & 1 and self.gt:
            res = (res + self.gt[0]) / 2
        return res


def __main():
    # med = Med(8)
    # med.add(6)
    # med.add(-2)
    med = Med(randint(-20, 20))
    for _ in range(12):
        med.add(randint(-20, 20))


if __name__ == '__main__':
    __main()
