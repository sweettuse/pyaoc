
from itertools import chain, repeat


def _get_spaces(regular_len, num_extra):
    extras = chain(num_extra * ' ', repeat(''))
    while True:
        yield regular_len * ' ' + next(extras)


def _join_sentence(words, num_spaces) -> str:
    num_gaps = len(words) - 1
    if not num_gaps:
        return words[0] + num_spaces * ' '
    
    spaces = _get_spaces(*divmod(num_spaces, num_gaps))
    res = []
    for w in words:
        res.append(w)
        res.append(next(spaces))
    res.pop()
    return ''.join(res)


def yield_words(words, max_width):
    cur_words = []
    cur_letters = 0


    for l, w in zip(map(len, words), words):
        next_letters = cur_letters + l
        next_total = next_letters + len(cur_words)  # add in spaces

        if next_total <= max_width:
            cur_words.append(w)
            cur_letters += l
        else:
            yield _join_sentence(cur_words, max_width - cur_letters)
            cur_words = [w]
            cur_letters = l

    if cur_words:
        res = ' '.join(cur_words)
        yield res + (max_width - len(res)) * ' '
        
def fullJustify(words: list[str], max_width: int) -> list[str]:
    return list(yield_words(words, max_width))

        
samples = (
    (["This", "is", "an", "example", "of", "text", "justification."], 16),
)

for v in samples:
    print('=======')
    print('\n'.join(fullJustify(*v)))