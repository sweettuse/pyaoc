# https://leetcode.com/problems/concatenated-words/
from __future__ import annotations
from dataclasses import dataclass, field
from functools import cache, cached_property
from typing import Iterable


@dataclass
class Node:
    char: str
    children: dict[str, Node] = field(default_factory=dict)
    is_word: bool = False

    def add_word(self, s: str) -> None:
        if not s:
            return
        cur, *rest = s
        if not (n := self.children.get(cur)):
            n = self.children[cur] = Node(cur)

        if not rest:
            n.is_word = True
            return

        return n.add_word(rest)


class Trie:
    def __init__(self) -> None:
        self.parent: Node = Node('')

    @classmethod
    def from_words(cls, words: Iterable[str]):
        res = cls()
        for w in words:
            res.add_word(w)
        return res

    def add_word(self, s: str):
        self.parent.add_word(s)

    def get_prefixes(self, s: str):
        n = self.parent
        res = set()
        for i, c in enumerate(s):
            if not (child := n.children.get(c)):
                break

            if child.is_word:
                res.add(s[: i + 1])

            n = child

        return frozenset(res)

    def is_compound(self, word: str, exclude_perfect_match=True) -> bool:
        if not word and not exclude_perfect_match:
            return True

        prefixes = self.get_prefixes(word)
        if exclude_perfect_match:
            prefixes -= {word}

        return any(self.is_compound(word[len(w) :], False) for w in prefixes)


def _test_add():
    trie = Trie()
    trie.add_word('jeb')
    trie.add_word('jebby')
    assert 'jeb' in trie
    assert 'tuse' not in trie
    assert 'jebb' not in trie
    assert 'jebby' in trie
    print('woweee')
    return trie


def _test_prefixes(trie: Trie):
    trie.add_word('tuse')
    assert trie.get_prefixes('jebbinald') == {'jeb'}
    assert trie.get_prefixes('jebby') == {'jeb', 'jebby'}


def _test_compound():
    words = ['jeb', 'tuse', 'jebtuse', 'jebtusetuse', 'jebtusetusejebtuse']
    trie = Trie.from_words(words)
    for w in words:
        if trie.is_compound(w):
            print(w)

def _test_stupid():
    trie = Trie.from_words([''])

def compound_words(words: list[str]) -> list[str]:
    pass


def __main():
    # trie = _test_add()
    # _test_prefixes(trie)
    _test_compound()


if __name__ == '__main__':
    __main()
