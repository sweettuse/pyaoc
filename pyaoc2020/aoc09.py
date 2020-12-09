from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

# window, data = 5, [int(v) for v in read_file('09.test', 2020)]
# window, data = 25, [int(v) for v in read_file('09.pat', 2020)]
window, data = 25, [int(v) for v in read_file(9, 2020)]
print(min(data), max(data))


def _is_match(pool, target):
    return any((res := target - p) in pool and res != p for p in pool)


def part1():
    pool = set(data[:window])
    for idx, v in enumerate(data[window:], window):
        if not _is_match(pool, v):
            return v
        pool.remove(data[idx - window])
        pool.add(data[idx])


def part2(target):
    i, j = 0, 1
    cur = data[i] + data[j]
    while cur != target:
        if cur < target:
            j += 1
            cur += data[j]
        else:
            cur -= data[i]
            i += 1
    rng = data[i: j + 1]
    return min(rng) + max(rng)


@timer
def __main():
    invalid = part1()
    print(invalid)
    print(part2(invalid))
    return invalid


if __name__ == '__main__':
    inv = __main()
