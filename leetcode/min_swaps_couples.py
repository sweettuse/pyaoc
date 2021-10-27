__author__ = 'acushner'

# https://leetcode.com/problems/couples-holding-hands/
import string
from collections import defaultdict

couple_ids = sorted(string.ascii_letters)


def min_swaps_couples(row):
    couple_loc_map = defaultdict(set)
    for loc, couple_num in enumerate(row):
        couple_loc_map[couple_ids[couple_num // 2]].add(loc // 2)

    return couple_loc_map


def __main():
    row = [0, 2, 1, 4, 3, 6, 7, 5]
    print(min_swaps_couples(row))
    pass


if __name__ == '__main__':
    __main()
