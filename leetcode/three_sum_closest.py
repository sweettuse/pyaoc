from bisect import bisect_left
from collections import Counter
from itertools import combinations
from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        diffs = sorted(((target - n), n) for n in nums)
        new_targets = [v[0] for v in diffs]
        used = [v[1] for v in diffs]
        print(new_targets)

        counts = Counter(nums)
        min_diff = float('inf')
        three_sum = None

        def _update_if_necessary(idx):
            nonlocal min_diff, three_sum
            abs_diff = abs(new_targets[idx] - v1 - v2)
            if abs_diff < min_diff:
                v_used = used[idx]
                cur_used = Counter((v1, v2, v_used))
                if all(total <= counts[u] for u, total in cur_used.items()):
                    three_sum = v1 + v2 + v_used
                    min_diff = abs_diff

        for v1, v2 in combinations(nums, 2):
            idx = bisect_left(new_targets, v1 + v2)
            if idx < len(nums):
                _update_if_necessary(idx)

            if idx > 0:
                _update_if_necessary(idx - 1)
        return three_sum


class Solution2():
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        res = None
        min_diff = float('inf')
        for i, v1 in zip(range(len(nums) - 2), nums):
            j = i + 1
            k = len(nums) - 1
            while j < k:
                cur = v1 + nums[j] + nums[k]
                cur_diff = abs(target - cur)
                if cur_diff < min_diff:
                    res = cur
                    min_diff = cur_diff

                if cur == target:
                    break

                if cur < target:
                    j += 1
                else:
                    k -= 1
        return res


def __main():
    nums = [-1, 2, 1, -4]
    target = 1
    print(Solution().threeSumClosest(nums, target))
    print(Solution2().threeSumClosest(nums, target))
    pass


if __name__ == '__main__':
    __main()
