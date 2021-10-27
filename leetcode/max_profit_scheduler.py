__author__ = 'acushner'

# https://leetcode.com/problems/maximum-profit-in-job-scheduling/
from bisect import bisect_left, bisect_right
from collections import defaultdict
from operator import itemgetter, attrgetter
from typing import List, NamedTuple
from functools import lru_cache

from pyaoc2019.utils import timer


class Job(NamedTuple):
    start: int
    end: int
    profit: int


class Solution:
    @timer
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(set(map(Job, startTime, endTime, profit)))
        print(len(jobs))

        def _can_run_sequentially(j1, j2):
            """assume j1 < j2 due to sorted jobs"""
            return j1.end <= j2.start

        @lru_cache(len(jobs))
        def _schedule(idx=0):
            """return max profit from this index"""
            if idx >= len(jobs):
                return 0

            cur_job = jobs[idx]
            paired_job_idxs = (i for i in range(idx + 1, len(jobs)) if _can_run_sequentially(cur_job, jobs[i]))
            return cur_job.profit + max(map(_schedule, paired_job_idxs), default=0)

        return max(_schedule(i) for i in range(len(jobs)))


def schedule(starts: List[int], ends: List[int], profits: List[int]):
    min_profit = lambda: float('-inf')
    start_times = sorted(set(starts))
    start_to_profit = defaultdict(min_profit)

    # could we use a better underlying data structure - like a bin search tree
    jobs = sorted(set(map(Job, starts, ends, profits)), key=itemgetter(1, 0))
    print(jobs)

    while jobs:
        cur = jobs.pop()
        cache_idx = bisect_left(start_times, cur.end)
        print(cur)

        # adding at end
        if cache_idx == len(start_times):
            start_to_profit[cur.start] = max(cur.profit, start_to_profit[cur.start])
        else:
            print(start_times[cache_idx])
            cur_max = start_to_profit[cur.start]
            start_to_profit[cur.start] = max(cur_max, cur.profit + start_to_profit[start_times[cache_idx]])
        print(start_to_profit)

    return max(start_to_profit.values())


@timer
def schedule2(starts: List[int], ends: List[int], profits: List[int]):
    jobs = sorted(map(Job, starts, ends, profits))
    starts = sorted(starts)
    next_possible_job = {j: bisect_left(starts, j.end) for j in jobs}

    @lru_cache(len(jobs))
    def _schedule(idx):
        if idx == len(jobs):
            return 0

        j = jobs[idx]

        return max(_schedule(idx + 1), j.profit + _schedule(next_possible_job[j]))

    return _schedule(0)


@timer
def schedule3(starts: List[int], ends: List[int], profits: List[int]):
    jobs = sorted(map(Job, starts, ends, profits))
    starts = sorted(starts)
    n = len(jobs)
    next_possible_job = {j: bisect_left(starts, j.end) for j in jobs}
    res = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        j = jobs[i]
        res[i] = max(res[i + 1], j.profit + res[next_possible_job[j]])

    return res[0]


def run_big():
    import sys
    sys.setrecursionlimit(30000)
    with open('inputs/max_profit_scheduler') as f:
        starts, ends, profits = map(eval, f)
        print(len(starts))
        print(schedule2(starts, ends, profits))
        print(schedule3(starts, ends, profits))


def __main():
    return run_big()
    starts = [1, 2, 3, 3]
    ends = [3, 4, 5, 6]
    profits = [50, 10, 40, 70]

    starts = [1, 2, 3, 4, 6]
    ends = [3, 5, 10, 6, 9]
    profits = [20, 20, 100, 70, 60]
    print(schedule2(starts, ends, profits))
    pass


if __name__ == '__main__':
    __main()
