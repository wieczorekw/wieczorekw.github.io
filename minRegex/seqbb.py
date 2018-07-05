from heapq import *
from FAdo.reex import *
import random
import sys

sys.setrecursionlimit(2000)
infinity = float('infinity')
Sigma = {'a', 'b', 'c', 'd'}  # 'v', '@' not in Sigma
Omega = '*' + '+'*(len(Sigma) - 1) + "".join(Sigma)
random.seed()

def alphabeticWidth(e):
    counter = 0
    for c in e:
        if c not in ['.', '+', '*']:
            counter += 1
    return counter

def children(u):

    def find_all_v():
        result = []
        for i in range(n):
            if u[i] == 'v':
                result.append(i)
        return result

    def isConcatArg(i):
        if i == 0:
            return False
        j = i
        stack_counter = 1
        while stack_counter > 0:
            j -= 1
            if u[j] == '*':
                stack_counter -= 1
            elif u[j] == '+' or u[j] == '.':
                stack_counter -= 2
            else:
                stack_counter += 1
        return u[j] == '.'

    n = len(u)
    idxs = find_all_v()
    r = random.choice(idxs)
    left = u[:r]
    right = u[r+1:]
    if not isConcatArg(r) and (r == 0 or u[r-1] != '*'):
        yield left + "@" + right  # @epsilon
    for a in Sigma:
        yield left + a + right
    yield left + "+vv" + right
    yield left + ".vv" + right
    if r == 0 or u[r-1] != '*':
        yield left + "*v" + right

def z(e, X, Y):

    def isConsistent(aut):
        return all(aut.evalWordP(w) for w in X) and not any(aut.evalWordP(w) for w in Y)

    if 'v' not in e:  # is complete
        regexpr = rpn2regexp(e.replace('@', "@epsilon"), sigma = Sigma)
        aut = regexpr.toDFA()
        return alphabeticWidth(e) if isConsistent(aut) else infinity
    else:  # is incomplete
        regexpr = rpn2regexp(e.replace('@', "@epsilon"), sigma = Sigma | {'v'})  # should be 'x', but 'v' is not worse
        aut = regexpr.toDFA()
        if any(aut.evalWordP(w) for w in Y):
            return infinity
        e2 = e.replace('v', Omega)
        regexpr = rpn2regexp(e2.replace('@', "@epsilon"), sigma = Sigma)
        aut = regexpr.toDFA()
        if not all(aut.evalWordP(w) for w in X):
            return infinity
        return alphabeticWidth(e)

def sequentialBB(S_plus, S_minus):
    q = []
    heappush(q, (1, "v"))
    min_width = infinity
    current_best = None
    while q:
        _, u = heappop(q)
        # print(u)
        for e in children(u):
            if alphabeticWidth(e) >= min_width:
                break
            z_e = z(e, S_plus, S_minus)
            if z_e < min_width:
                if "v" not in e:
                    min_width = z_e
                    current_best = e
                else:
                    heappush(q, (z_e, e))
    return current_best
