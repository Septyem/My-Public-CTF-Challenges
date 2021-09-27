#!/usr/bin/python3
import lark
import random

f = open('lark.lark')
s = f.read()
parser = lark.Lark(s)
f = open('grammar')
s = f.read()
g = parser.parse(s)
p2 = lark.Lark(s)
assert g.children[7].children[0].value == 'expression'
assert g.children[8].children[0].value == 'statement'

def collect_cov(ast):
    cov = 0
    if isinstance(ast, lark.tree.Tree):
        for ch in ast.children:
            cov |= collect_cov(ch)
        if ast.data.startswith('cov_'):
            num = int(ast.data[4:])
            cov |= (1<<num)
    return cov

def genone(target):
    sz = len(g.children[7+target].children[2].children)
    idx = random.randint(0,sz-1)
    rule = g.children[7+target].children[2].children[idx].children[0]
    res = ''
    for i in range(len(rule.children)):
        t = rule.children[i].children[0].type
        v = rule.children[i].children[0].value
        if t == 'STRING':
            res += ' '+v[1:-1]+' '
        elif t == 'TOKEN':
            if v == 'NUMBER' or v == 'DIGIT':
                res += ' 1 '
            elif v == 'LETTER' or v == 'WORD':
                res += ' a '
        elif t == 'RULE':
            if v == 'expression':
                res += genone(0)
            elif v == 'statement':
                res += genone(1)
    return res


def gensample():
    res = ''
    for i in range(8):
        res += genone(1)+'\n'
    return res

found = set()
while len(found) < 0x1000:
    one = gensample()
    res = p2.parse(one)
    cov = collect_cov(res)
    if bin(cov).count('1') >= 20 and cov not in found:
        found.add(one)

print('|'.join(found))
