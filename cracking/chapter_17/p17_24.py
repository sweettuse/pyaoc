__author__ = 'acushner'

# 17.24 Max Submatrix: Given an NxN matrix of positive and negative integers, write code to find the
# submatrix with the largest possible sum.
from itertools import accumulate, combinations, product


def by_rows(m):
    for r in m:
        print(r)
    print(20 * '=')


def transpose(m):
    return [[row[c] for row in m] for c in range(len(m))]


def _create_summed_area_table(m):
    m = [list(accumulate(row)) for row in m]
    m = [list(accumulate(row)) for row in transpose(m)]
    return transpose(m)


def max_submatrix(m):
    def _calc_range(p1, p2):
        pass

    sat = _create_summed_area_table(m)
    by_rows(sat)


def __main():
    m = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    points = product(range(len(m)), repeat=2)
    print(list(combinations(points, 2)))
    # by_rows(m)
    # max_submatrix(m)
    # print(sum(c for row in m for c in row))

    pass


if __name__ == '__main__':
    __main()
