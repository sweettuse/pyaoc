__author__ = 'acushner'


# 1.6 String Compression: Implement a method to perform basic string compression using the counts
# of repeated characters. For example, the string aabcccccaaa would become a2b1c5a3. If the
# "compressed" string would not become smaller than the original string, your method should return
# the original string. You can assume the string has only uppercase and lowercase letters (a - z).
# Hints:#92, #110
def compress(s) -> str:
    if not s:
        return ''

    cur, *s = s
    count = 1
    res = []

    def _add(cur, count):
        res.append((cur, str(count)))

    for c in s:
        if c != cur:
            _add(cur, count)
            cur, count = c, 0
        count += 1

    _add(cur, count)
    return ''.join(''.join(t) for t in res)


def __main():
    print(compress('aabcccccaaa'))

    pass


if __name__ == '__main__':
    __main()
