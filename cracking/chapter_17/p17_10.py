__author__ = 'acushner'


# 17 .10 Majority Element: A majority element is an element that makes up more than half of the items in
# an array. Given a positive integers array, find the majority element. If there is no majority element,
# return-1. Do this inO(N) time and 0(1) space.
# EXAMPLE
# Input:
# 1 2 5 9 5 9 5 5 5
# Output:
# 5
# Hints: #522, #566, #604, #620, #650

def maj_elt(l: list[int]):
    l = l.copy()
    max_l = max(l) + 1
    for v in l:
        l[hash(v % max_l) % len(l)] += max_l

    max_hash, max_idx = max(((v - v % max_l) // max_l, i) for i, v in enumerate(l))
    # print(f'{max_idx=} {max_hash=}')
    to_consider = []
    seen = set()
    for i, v in enumerate(l):
        # print('idx', i, v, v % max_l, max_l)
        v %= max_l
        if hash(v) % len(l) == max_idx and v not in seen:
            seen.add(v)
            # print('how', v, )

            total = sum((check_v % max_l) == v for check_v in l)
            # print(f'{total = }')
            if total > len(l) / 2:
                return v


def maj_elt_with_help(l: list[int]):
    def _helper():
        cur_count = 0
        cur_num = None
        for v in l:
            if not cur_count:
                cur_num = v

            if v == cur_num:
                cur_count += 1
            else:
                cur_count -= 1
        return cur_num

    v = _helper()
    if sum(check_v == v for check_v in l) > len(l) / 2:
        return v


def __main():
    l = [1, 42, 42, 6, 42, 17, 42, 42, 63, 12, 42, 42, 42, 3, 3]
    l = [7, 1, 7, 1]
    # print(len(l))
    print('holy shit', maj_elt(l))
    # print(maj_elt_with_help(l))

    pass


if __name__ == '__main__':
    __main()
