__author__ = 'acushner'

# 17.22 Word Transformer: Given two words of equal length that are in a dictionary, write a method to
# transform one word into another word by changing only one letter at a time. The new word you get
# in each step must be in the dictionary.
# EXAMPLE
# Input: DAMP, LIKE
# Output: DAMP-> LAMP-> LIMP-> LIME-> LIKE
# Hints: #506, #535, #556, #580, #598, #618, #738
from collections import deque, defaultdict
from dataclasses import dataclass
from functools import cached_property, lru_cache
from typing import Optional, NamedTuple, Union


def _is_adj(w1, w2):
    num_diffs = 0
    for c1, c2 in zip(w1, w2):
        num_diffs += c1 != c2
        if num_diffs > 1:
            return False

    return True


def _get_adj(target, words, seen):
    return (w for w in words if _is_adj(target, w) and w not in seen)


class Node(NamedTuple):
    parent: Optional['Node']
    word: str

    def __iter__(self):
        cur = self
        while cur:
            yield cur
            cur = cur.parent


def word_path(start, end, words: set[str]) -> list[str]:
    cur = head = Node(None, start)
    nodes = deque(head)
    while nodes:
        cur = nodes.popleft()
        if cur.word == end:
            break
        seen = {n.word for n in cur}
        nodes.extend(Node(cur, w) for w in _get_adj(cur.word, words, seen))

    res = [n.word for n in cur]
    res.reverse()
    return res


class WordPathFast:
    def __init__(self, words: set[str]):
        self.words = words
        self._word_to_sim_map = self._create_word_to_sim_map(self.words)

    @staticmethod
    @lru_cache
    def _word_to_wildcards(w: str) -> set[str]:
        """'abc' -> {'_bc', 'a_c', 'ab_'}"""
        cur = list(w)
        res = set()
        for i, c in enumerate(cur):
            cur[i] = '_'
            res.add(''.join(cur))
            cur[i] = c
        return res

    @staticmethod
    def _create_word_to_sim_map(words):
        res = defaultdict(set)
        for word in words:
            for wildcard in WordPathFast._word_to_wildcards(word):
                res[wildcard].add(word)
        return res

    def _get_one_away(self, word: str):
        return set().union(*(self._word_to_sim_map[w] for w in self._word_to_wildcards(word)))

    def _bfs(self, node: Node):
        cur = {node.word: node}
        yield cur

        while True:
            res = {}
            for n in cur.values():
                seen = {cur_n.word for cur_n in n}
                res.update((neighbor, Node(n, neighbor))
                           for neighbor in self._get_one_away(n.word)
                           if neighbor not in seen)
            yield res
            cur = res

    def bfs(self, start, end):
        from_start = Node(None, start)
        from_end = Node(None, end)

        start_nodes = self._bfs(from_start)
        end_nodes = self._bfs(from_end)

        def _check_match():
            inter = cur_start.keys() & cur_end

            if inter:
                meet = inter.pop()
                start_path = [n.word for n in cur_start[meet]]
                start_path.reverse()
                return start_path[:-1] + [n.word for n in cur_end[meet]]

        cur_end = next(end_nodes)
        while True:
            cur_start = next(start_nodes)
            if res := _check_match():
                return res

            cur_end = next(end_nodes)
            if res := _check_match():
                return res


def word_path_fast(start, end, words: set[str]) -> list[str]:
    """use 2-way BFS"""

    wpf = WordPathFast(words)
    return wpf.bfs(start, end)


def __main():
    start = 'DAMP'
    end = 'LIKE'
    words = set('damp lamp limp lime like'.upper().split())
    print(word_path(start, end, words))
    print(word_path_fast(start, end, words))
    pass


if __name__ == '__main__':
    __main()
