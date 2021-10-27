__author__ = 'acushner'

# https://leetcode.com/problems/longest-valid-parentheses/
from itertools import accumulate


def longest_valid_parens(s):
    if not s:
        return 0
    stack = []
    start = float('inf')
    cur_max = 0
    new_stack_time = True
    for i, p in enumerate(s):
        if not stack and new_stack_time:
            start = i
            new_stack_time = False
        if p == '(':
            stack.append(p)
        elif p == ')':
            if stack:
                stack.pop()
            else:
                new_stack_time = True
                cur_max = max(i - start, cur_max)
    if not new_stack_time:
        cur_max = max(cur_max, i - start - len(stack) + 1)
    return cur_max


def longest_valid_parens(s):
    stack = []
    stack_size = []
    for i, p in enumerate(s):
        offset = 0
        if p == '(':
            stack.append(p)
        elif stack:
            stack.pop()
        else:
            offset = -1
        stack_size.append(len(stack) + offset)
    return stack_size
    # return list(accumulate(1 if c == '(' else -1 for c in s))

def longest_valid_parens(s):
    stack = [-1]
    res = 0
    for i, p in enumerate(s):
        if p == '(':
            stack.append(i)
        else:
            pass


def __main():
    s = '(((((('
    t = '' \
        ''

    # s = ')(())(()))'
    # s = '()())'
    # s = "(())(()())))"
    print(list(s))
    print([str(v) for v in longest_valid_parens(s)])
    pass


if __name__ == '__main__':
    __main()
