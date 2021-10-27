__author__ = 'acushner'

# 17.15 Longest Word: Given a list of words, write a program to find the longest word made of component words
# in the list.
# EXAMPLE
# Input:cat, banana, dog, nana, walk, walker, dogwalker
# Output: dogwalker
# Hints: #475, #499, #543, #589

from typing import Set, Optional, Dict, Iterable


def longest_composed_word(words: Set[str]) -> Optional[str]:
    words = words.copy()

    def _find(cur):
        if not cur:
            return True

        return any(cur.startswith(component)
                   and _find(cur[len(component):])
                   for component in words)

    by_len = sorted(words, key=len, reverse=True)
    for w in by_len:
        words.remove(w)
        if _find(w):
            return w
    return


class Trie:
    def __init__(self, char=''):
        self.char = char
        self.children: Dict[str, Trie] = {}
        self.is_terminal = False
        self._terminal_word = None

    @classmethod
    def from_words(cls, words: Iterable[str]):
        t = cls()
        for w in words:
            t.add(w)

        return t

    def add(self, word):
        return self._add(word, word)

    def _add(self, word, full_word):
        if not word:
            self.is_terminal = True
            self._terminal_word = full_word
            return

        c, *rest = word
        if c in self.children:
            t = self.children[c]
        else:
            t = self.children[c] = Trie(c)

        t._add(rest, full_word)
        return self

    def __iter__(self):
        for t in self.children.values():
            if t.is_terminal:
                yield t
            yield from t

    def __str__(self):
        return f'Trie({self._terminal_word})'

    __repr__ = __str__

    def __getitem__(self, item: str):
        if len(item) != 1:
            raise ValueError('item too long')

        return self.children[item]

    @property
    def words(self):
        return list(self)


def with_trie(words):
    head = Trie.from_words(words)
    print(list(head))
    by_len = sorted(words, key=len, reverse=True)
    for w in by_len:
        print(w, w[0])
        print(head[w[0]].words)


def __main():
    words = {'cat', 'banana', 'dog', 'nana', 'walk', 'walker', 'dogwalker'}
    words = {'cat', 'banana', 'dog', 'nana', 'walk', 'walker', 'dogwalker', 'bananawalkerx',
             'xnanabananananawalkerbanana'}

    print(longest_composed_word(words))
    with_trie(words)


if __name__ == '__main__':
    __main()
