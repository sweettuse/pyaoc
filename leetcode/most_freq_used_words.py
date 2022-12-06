# https://www.codewars.com/kata/51e056fe544cf36c410000fb/train/python

from collections import Counter
from itertools import chain
from operator import itemgetter
import string


valids = set(string.ascii_lowercase) | {"'"}

def _split(text):
    cur = []
    for c in text.lower():
        if c in valids:
            cur.append(c)
        else:
            if cur and set(cur) != {"'"}:
                yield ''.join(cur)
            cur.clear()
    if cur:
        yield ''.join(cur)

def top_3_words(text):
    c = Counter(_split(text))
    return [v[0] for v in sorted(c.items(), key=itemgetter(1), reverse=True)[:3]]


import re
from itertools import chain

possible = set(range(10))
def solve_runes(runes):
    runes = runes.replace('=', '==')
    disallowed = set(map(int, chain.from_iterable(re.findall('\d+', runes))))
    zero_possible = re.findall('\d+', runes.replace('?', '0'))
    if any(s.startswith('0') and len(s) > 1 for s in zero_possible):
        disallowed |= {0}
    
    for v in sorted(possible - disallowed):
        s = runes.replace('?', str(v))
        print(s)
        if eval(s):
            return v
    return -1

# print(solve_runes('?*11=??'))
# print(solve_runes('-194*-4?68=847?92'))
# print(solve_runes('5650--?1388=?7038'))



def _do_the_diff(c: list[str]) -> str:
    if 'x' not in c:
        return '0'

    res = ''.join(c)
    if res.endswith('x'):
        return res[:-1] or '1'
    
    coeff, exp = res.split('x^')
    if not coeff or coeff == '-':
        coeff += '1'

    coeff, exp = int(coeff), int(exp)
    if exp == 0:
        return ''
    if exp == 1:
        return str(coeff)
    
    return f'{coeff * exp}x**{exp - 1}'


def parse(eq: str):
    cur = []
    for c in eq:
        if cur and c in {'+', '-'}:
            yield _do_the_diff(cur)
            yield c
            cur = []
        else:
            cur.append(c)
    if cur:
        yield _do_the_diff(cur)
    

def differentiate(equation, point):
    equation = equation.replace('--', '+')
    diff = ' '.join(parse(equation))
    r = diff.replace('x', f'*({point})')
    return eval(r)
    

print(differentiate('-7x^5+22x^4-55x^3-94x^2+87x-56', -3))
# print(differentiate("x^2-x", 3))


def last_digit(vals: list):
    ones = [int(str(v)[-1]) for v in vals]
    twos = [int(str(v)[-2:]) for v in vals]
    
    while len(ones) > 1:
        _, exp2 = ones.pop(), twos.pop()
        base1, _ = ones.pop(), twos.pop()
        res = str(base1 ** exp2)
        ones.append(int(res[-1]))
        twos.append(int(res[-2:]))

    if len(ones) == 1:
        return ones[0]
    

def last_digit(vals: list):
    twos = [int(str(v)[-2:]) for v in vals]
    
    while len(twos) > 1:
        exp = twos.pop()
        base = twos.pop()
        res = str(base ** exp)
        twos.append(int(res[-2:]))

    if len(twos) == 1:
        return twos[0] % 10
    


samples = (
    ([937640, 767456, 981242], 0),
    ([123232, 694022, 140249], 6),
    ([499942, 898102, 846073], 6),
)


for s in samples:
    print(last_digit(s[0]))