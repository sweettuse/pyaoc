from collections import Counter, defaultdict
import heapq
from typing import Optional
class Heap:
    def __init__(self, size: int) -> None:
        self.size = size
        self.h = []
    
    def push_if_relevant(self, v) -> bool:
        v = -abs(v)
        res = True

        if not self.full:
            heapq.heappush(self.h, v)
        elif v > self.h[0]:
            heapq.heappushpop(self.h, v)
        else:
            res = False

        return res

    def __iter__(self):
        data = self.h.copy()
        return reversed([heapq.heappop(data) for _ in range(len(data))])
    
    def __getitem__(self, item):
        return -self.h[item]

    @property
    def full(self) -> bool:
        return len(self.h) >= self.size


class Node:
    def __init__(self, key, count):
        self.key = key
        self.count = count
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
    
    def insert(self, key, count):
        if key == self.key:
            self.count += count
        elif key < self.key:
            if self.left:
                self.left.insert(key, count)
            else:
                self.left = Node(key, count)
        else:
            if self.right:
                self.right.insert(key, count)
            else:
                self.right = Node(key, count)

class Tree:
    def __init__(self):
        self.head = None
    
    def insert(self, key, count):
        if self.head is None:
            self.head = Node(key, count)
        else:
            self.head.insert(key, count)


def sdp2(nums: list[int], k: int) -> int:
    c = sorted(Counter(nums).items())

    for end, (r, rcount) in enumerate(c):
        for start in range(end - 1, -1, -1):
            l, lcount = c[start]
            if not h.push_if_relevant((r - l) * rcount * lcount):
                break

    return h[0]


    tree = Node()

class Heap2:
    def __init__(self, size):
        self.size = size
        self.counts = defaultdict(int)
        self.minh = []
        self.maxh = []
        self.total_added = 0
    
    def push_if_relevant(self, v, count=1) -> bool:
        v = -abs(v)
        res = True
        self.total_added += count
        if v in self.counts:
            self.counts[v] += count
        

            heapq.heappush(self.h, v)
        elif v > self.h[0]:
            heapq.heappushpop(self.h, v)
        else:
            res = False

        return res

    





def smallestDistancePair(nums: list[int], k: int) -> int:
    h = Heap(k)
    if len(nums) < 2:
        return 
    nums = sorted(nums)
    counts = Counter(nums)

    right = enumerate(nums)
    
    for end, r in right:
        for l in range(end - 1, -1, -1):
            if not h.push_if_relevant(r - nums[l]):
                break

    return h[0]

        

samples = (
    # ([1,3,1], 1),
    # ([1,1,1], 2),
    # ([1,6,1], 3),
    ([9,10,7,10,6,1,5,4,9,8], 18),
)  # fmt: skip


for s in samples:
    print(smallestDistancePair(*s))


