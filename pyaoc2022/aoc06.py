from __future__ import annotations

from collections import Counter, defaultdict, deque
from functools import partial

from pyaoc2019.utils import read_file, take, timer


def parse_file(name):
    return read_file(name)[0]

time_multiple = partial(timer, n_times=100)

@time_multiple
def find_start_of_message(data, maxlen):
    """notes:
    
    - Counter is still slow
    - deque/set is faster until msg_len 7, then defaultdict starts to win
    """
    it = iter(data)

    d = deque(take(maxlen - 1, it), maxlen=maxlen)
    for i, c in enumerate(it, maxlen):
        d.append(c)
        if len(set(d)) == maxlen:
            return i


@time_multiple
def find_start_of_message_counter(data, total_len):
    it = iter(data)

    res = Counter(take(total_len - 1, it))
    for i, c in enumerate(it, total_len):
        res[c] += 1
        if len(res) == total_len:
            return i

        prev = data[i - total_len]
        res[prev] -= 1
        if not res[prev]:
            res.pop(prev)

@time_multiple
def find_start_of_message_ddict(data, total_len):
    it = iter(data)

    res = defaultdict(int)
    init = take(total_len - 1, it)

    for v in init:
        res[v] += 1

    for i, c in enumerate(it, total_len):
        res[c] += 1
        if len(res) == total_len:
            return i

        prev = data[i - total_len]
        res[prev] -= 1
        if not res[prev]:
            res.pop(prev)


data = parse_file(6)
print('================')
print('================')
print(find_start_of_message(data, 4))
print(find_start_of_message(data, 14))
print('================')
for size in range(4, 16):
    print(f"{size:-^30}")
    find_start_of_message(data, size)
    find_start_of_message_ddict(data, size)
    find_start_of_message_counter(data, size)
