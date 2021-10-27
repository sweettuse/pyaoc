__author__ = 'acushner'

# 16.3 Intersection: Given two straight line segments (represented as a start point and an end point),
# compute the point of intersection, if any.
# Hints:#465, #472, #497, #517, #527


# y = mx + b
# m = rise / run

# y1 = m1x1 + b1
# y2 = m2x2 + b2
# x1, y1 == x2, y2
# m1x1 + b1 == m2x2 + b2
# m1x - m2x = b2 - b1
# (m1 - m2)x = b2 - b1
# x = (b2 - b1) / (m1 - m2)
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class LineSeg(NamedTuple):
    p1: Point
    p2: Point

    @property
    def m_b(self):
        m = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
        b = self.p1.y - m * self.p1.x
        return m, b

    def x_between(self, x):
        p1, p2 = sorted(self)
        return p1.x <= x <= p2.x


def intersection(ls1: LineSeg, ls2: LineSeg):
    ls1, ls2 = sorted((ls1, ls2))
    m1, b1 = ls1.m_b
    m2, b2 = ls2.m_b

    if m1 == m2:
        if b1 != b2:
            return None, None

        for cur, other in ((ls1, ls2), (ls2, ls1)):
            for p in other:
                if cur.x_between(p.x):
                    return p
        return None, None

    else:
        x = (b2 - b1) / (m1 - m2)

    if ls1.x_between(x) and ls2.x_between(x):
        return x, m1 * x + b1
    return None, None


def __main():
    ls1 = LineSeg(Point(-1, -1), Point(0, 0))
    ls2 = LineSeg(Point(1, 1), Point(2, 2))
    print(intersection(ls1, ls2))
    pass


if __name__ == '__main__':
    __main()
