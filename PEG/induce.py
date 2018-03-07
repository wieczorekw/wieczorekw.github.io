from peg import *
from operator import or_
from functools import reduce

term = dict((chr(i), Terminal(chr(i))) for i in range(ord('a'), ord('z') + 1))

def left_quotient(a, W):
    result = set()
    for w in W:
        if w != '' and w[0] == a:
            result.add(w[1:])
    return result

def induce(X, Y):
    aX = set(x[0] for x in X if x != '')
    aY = set(y[0] for y in Y if y != '')
    exps = []
    for a in aX:
        lqX = left_quotient(a, X)
        lqY = left_quotient(a, Y)
        if a not in aY:
            exps.append(term[a])
        else:
            exps.append(term[a] >> induce(lqX, lqY))
    if exps == []:
        return ~reduce(or_, (term[a] for a in aY))
    if '' in X:
        exps.append(~reduce(or_, (term[a] for a in aY)) >> epsilon)
    return reduce(or_, exps)
