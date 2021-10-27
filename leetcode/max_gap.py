__author__ = 'acushner'


def max_gap(l):
    l = set(l)

    if len(l) < 2:
        return 0
    if len(l) == 2:
        return abs(l.pop() - l.pop())

    num_buckets = len(l) - 1
    min_val, max_val = min(l), max(l)

    if num_buckets == 1:
        return max_val - min_val

    diff = (max_val - min_val) // num_buckets
    buckets = [[] for _ in range(num_buckets)]
    for v in l:
        idx = min(num_buckets - 1, (v - min_val) // diff)
        buckets[idx].append(v)

    min_max_per_bucket = [(min(b), max(b)) for b in buckets if b]
    return max(abs(mx - mn) for (_, mx), (mn, _) in zip(min_max_per_bucket, min_max_per_bucket[1:]))


def __main():
    l = [3, 14, 15, 83, 6, 4, 19, 20, 40]
    l = [3, 6, 9, 1]
    l = [1, 1, 1, 1, 1, 5, 5, 5, 5, 5]
    print(max_gap(l))
    pass


if __name__ == '__main__':
    __main()
