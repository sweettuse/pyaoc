__author__ = 'acushner'


def len_of_longest_substr(s: str) -> int:
    if len(s) <= 1:
        return len(s)

    max_len = 0
    left = 0
    used = {}
    for right in range(len(s)):
        cur = s[right]
        if cur in used:
            left = max(used[cur] + 1, left)
        max_len = max(max_len, right - left + 1)
        used[cur] = right
    return max_len


def __main():
    print(len_of_longest_substr('abba'))
    pass


if __name__ == '__main__':
    __main()
