__author__ = 'acushner'

from functools import lru_cache
from heapq import heappop, heappush
from typing import List

# https://leetcode.com/problems/minimum-number-of-refueling-stops/
from pyaoc2019.utils import timer


@timer
def min_refuel_stops(target: int, start_fuel: int, stations: List[List[int]]) -> int:
    min_stops = float('inf')

    @lru_cache(None)
    def _rec(cur_idx=0, cur_fuel=start_fuel, cur_loc=0, total_stops=0):
        nonlocal min_stops
        if cur_loc + cur_fuel >= target:
            min_stops = min(total_stops, min_stops)
            return
        if total_stops >= min_stops:
            return

        can_make = []
        for i in range(cur_idx, len(stations)):
            pos, fuel = stations[i]
            if cur_fuel >= pos - cur_loc:
                can_make.append(i)
            else:
                break

        if not can_make:
            return

        can_make.sort(key=lambda i: -stations[i][1])
        # can_make.reverse()
        for i in can_make:
            pos, fuel = stations[i]
            _rec(i + 1, cur_fuel - (pos - cur_loc) + fuel, pos, total_stops + 1)

    _rec()
    print(_rec.cache_info())
    return min_stops if min_stops != float('inf') else -1


@timer
def minRefuelStops(self, target: int, start_fuel: int, stations: List[List[int]]) -> int:
    stations.append([target, 0])
    heap = []
    stops = 0
    cur_fuel = start_fuel
    cur_pos = 0
    for i in range(len(stations)):
        s = stations[i]
        while cur_pos + cur_fuel < s[0]:
            if not heap:
                return -1
            cur_fuel += (-heappop(heap))
            stops += 1

        cur_fuel = cur_fuel - (s[0] - cur_pos)
        cur_pos = s[0]

        heappush(heap, -s[1])

    if cur_pos + cur_fuel >= target:
        return stops
    return -1


def __main():
    target = 1000
    start_fuel = 36
    stations = [[7, 13], [10, 11], [12, 31], [22, 14], [32, 26], [38, 16], [50, 8], [54, 13], [75, 4], [85, 2],
                [88, 35], [90, 9],
                [96, 35], [103, 16], [115, 33], [121, 6], [123, 1], [138, 2], [139, 34], [145, 30], [149, 14],
                [160, 21],
                [167, 14], [188, 7], [196, 27], [248, 4], [256, 35], [262, 16], [264, 12], [283, 23], [297, 15],
                [307, 25],
                [311, 35], [316, 6], [345, 30], [348, 2], [354, 21], [360, 10], [362, 28], [363, 29], [367, 7],
                [370, 13],
                [402, 6], [410, 32], [447, 20], [453, 13], [454, 27], [468, 1], [470, 8], [471, 11], [474, 34],
                [486, 13],
                [490, 16], [495, 10], [527, 9], [533, 14], [553, 36], [554, 23], [605, 5], [630, 17], [635, 30],
                [640, 31],
                [646, 9], [647, 12], [659, 5], [664, 34], [667, 35], [676, 6], [690, 19], [709, 10], [721, 28],
                [734, 2], [742, 6],
                [772, 22], [777, 32], [778, 36], [794, 7], [812, 24], [813, 33], [815, 14], [816, 21], [824, 17],
                [826, 3],
                [838, 14], [840, 8], [853, 29], [863, 18], [867, 1], [881, 27], [886, 27], [894, 26], [917, 3],
                [953, 6], [956, 3],
                [957, 28], [962, 33], [967, 35], [972, 34], [984, 8], [987, 12]]
    print(min_refuel_stops(target, start_fuel, stations))
    print(minRefuelStops(None, target, start_fuel, stations))


if __name__ == '__main__':
    __main()


def __main():
    pass


if __name__ == '__main__':
    __main()
