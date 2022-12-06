# https://leetcode.com/problems/minimum-window-substring/

from collections import Counter, defaultdict, deque
from contextlib import suppress
from itertools import tee
from typing import Type


def min_window_orig(s: str, t: str) -> str:
    letters: dict[str, deque[int]] = {k: deque(maxlen=v) for k, v in Counter(t).items()}

    set_t = set(t)
    relevant = ((i, c) for i, c in enumerate(s) if c in set_t)

    unique_letters = len(letters)
    num_full_deques = 0

    seen: dict[int, Type[None]] = {}
    end = 0

    cur_start = lambda: next(iter(seen))

    for i, c in relevant:
        d = letters[c]
        if len(d) == d.maxlen:
            del seen[d[0]]
        elif len(d) == d.maxlen - 1:
            num_full_deques += 1
        d.append(i)
        seen[i] = None
        if num_full_deques == unique_letters:
            end = i
            break
    else:
        return ''

    start = cur_start()
    span = end - start
    best = start, end

    for i, c in relevant:
        seen[i] = None
        end = i

        d = letters[c]
        del seen[d[0]]

        d.append(i)
        new_start = cur_start()
        new_span = end - new_start
        if new_span < span:
            span = new_span
            best = new_start, end

    start, end = best
    return s[start : end + 1]


def min_window_derived_from_leetcode_answer(s: str, t: str) -> str:
    if not s or not t:
        return ''

    target_counts = Counter(t)
    cur_counts = defaultdict(int)
    required = len(target_counts)
    filled = 0

    left, right = tee((i, c) for i, c in enumerate(s) if c in target_counts)

    span = float('inf')
    best = None

    for end, c in right:
        cur_counts[c] += 1
        if cur_counts[c] == target_counts[c]:
            filled += 1

        if filled == required:
            for start, c in left:
                if (new_span := end - start) < span:
                    span = new_span
                    best = start, end
                cur_counts[c] -= 1
                if cur_counts[c] < target_counts[c]:
                    filled -= 1
                    break

    if best is not None:
        start, end = best
        return s[start : end + 1]
    return ''


def min_window_with_fewer_vars(s: str, t: str) -> str:
    if not s or not t:
        return ''

    needed = Counter(t)
    unfilled = len(needed)

    span = float('inf')
    best = None

    left, right = tee((i, c) for i, c in enumerate(s) if c in needed)
    for end, c in right:
        needed[c] -= 1

        if not needed[c]:
            unfilled -= 1

        if unfilled:
            continue

        for start, c in left:
            if (new_span := end - start) < span:
                span = new_span
                best = start, end

            needed[c] += 1
            if needed[c] > 0:
                unfilled += 1
                break

    if best is None:
        return ''

    start, end = best
    return s[start : end + 1]


def minWindow(self, s, t):
    """actual ugly-ass answer from leetcode"""
    if not t or not s:
        return ''

    dict_t = Counter(t)

    required = len(dict_t)

    # Filter all the characters from s into a new list along with their index.
    # The filtering criteria is that the character should be present in t.
    filtered_s = []
    for i, char in enumerate(s):
        if char in dict_t:
            filtered_s.append((i, char))

    l, r = 0, 0
    formed = 0
    window_counts = {}

    ans = float('inf'), None, None

    # Look for the characters only in the filtered list instead of entire s. This helps to reduce our search.
    # Hence, we follow the sliding window approach on as small list.
    while r < len(filtered_s):
        character = filtered_s[r][1]
        window_counts[character] = window_counts.get(character, 0) + 1

        if window_counts[character] == dict_t[character]:
            formed += 1

        # If the current window has all the characters in desired frequencies i.e. t is present in the window
        while l <= r and formed == required:
            character = filtered_s[l][1]

            # Save the smallest window until now.
            end = filtered_s[r][0]
            start = filtered_s[l][0]
            if end - start + 1 < ans[0]:
                ans = (end - start + 1, start, end)

            window_counts[character] -= 1
            if window_counts[character] < dict_t[character]:
                formed -= 1
            l += 1

        r += 1
    return '' if ans[0] == float('inf') else s[ans[1] : ans[2] + 1]


samples = [('ADOBECODEBANC', 'ABC'), ('a', 'a'), ('a', 'aa'), ('bba', 'ab')]


for v in samples:
    print(min_window_derived_from_leetcode_answer(*v))

