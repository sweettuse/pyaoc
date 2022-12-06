from __future__ import annotations

from collections import Counter, defaultdict, deque

from pyaoc2019.utils import read_file, take


def parse_file(name):
    return read_file(name)[0]


def find_start_of_message(data, maxlen):
    it = iter(data)

    d = deque(take(maxlen - 1, it), maxlen=maxlen)
    for i, c in enumerate(it, maxlen):
        d.append(c)
        if len(set(d)) == maxlen:
            return i


def find_start_of_message_dict(data, total_len):
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


data = parse_file(6)
print(find_start_of_message(data, 4))
print(find_start_of_message_dict(data, 4))
print(find_start_of_message(data, 14))
print(find_start_of_message_dict(data, 14))
