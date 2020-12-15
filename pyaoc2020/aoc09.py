from itertools import accumulate, islice, chain

from pyaoc2019.utils import read_file, timer, localtimer

__author__ = 'acushner'

# window, data = 5, [int(v) for v in read_file('09.test', 2020)]
# window, data = 25, [int(v) for v in read_file('09.pat', 2020)]
window, data = 25, [int(v) for v in read_file(9, 2020)]


def _is_match(pool, target):
    return any((res := target - p) in pool and res != p for p in pool)


def part1():
    pool = set(data[:window])
    for idx, v in enumerate(data[window:], window):
        if not _is_match(pool, v):
            return v
        pool.remove(data[idx - window])
        pool.add(data[idx])


@timer
def part2(target):
    """inchworm range"""
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
def part2_brute_smartish(target):
    """using slightly smart brute force"""
    for i in range(len(data)):
        cur = data[i]
        for j in range(i + 1, len(data)):
            cur += data[j]
            if cur > target:
                break
            if cur == target:
                rng = data[i: j + 1]
                return min(rng) + max(rng)


@timer
def part2_cumsum(target):
    """using cum sum"""
    sum_data = list(accumulate([0] + data))
    for i, i_val in enumerate(sum_data):
        for j, j_val in enumerate(islice(sum_data, i + 1, None), i + 1):
            diff = j_val - i_val
            if diff > target:
                break
            if diff == target:
                rng = data[i: j + 1]
                return min(rng) + max(rng)


@timer
def part2_brute(target):
    for i in range(len(data)):
        for j in range(len(data)):
            rng = data[i: j + 1]
            if sum(rng) == target:
                return min(rng) + max(rng)


@timer
def __main():
    invalid = part1()
    print(invalid)
    print(part2(invalid))
    print(part2_brute(invalid))
    print(part2_brute_smartish(invalid))
    print(part2_cumsum(invalid))


if __name__ == '__main__':
    __main()
