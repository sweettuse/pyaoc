import os
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush

print(os.getcwd())
with open("./inputs/15") as f:
    data = [list(map(int, line)) for line in f.read().strip().split("\n")]


heap = [(0, 0, 0)]
seen = {(0, 0)}
while heap:
    distance, x, y = heappop(heap)
    if x == 5 * len(data) - 1 and y == 5* len(data[0]) - 1:
        print(distance)
        break

    for dx, dy in ((0, 1), (0 , -1), ( 1, 0), (-1, 0)):
        x_, y_ = x + dx, y + dy
        if (x_, y_) in seen:
            continue
        if x_ < 0 or y_ < 0 or x_ >= 5 * len(data) or y_ >= 5 * len(data):
            continue

        a, am = divmod(x_, len(data))
        b, bm = divmod(y_, len(data[0]))
        n = ((data[am][bm] + a + b) - 1) % 9 + 1

        seen.add((x_, y_))
        heappush(heap, (distance + n, x_, y_))

