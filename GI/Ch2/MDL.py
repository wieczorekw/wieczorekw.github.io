from Preliminaries2 import *
from math import log
from FAdo.fa import *

def memoize(function):
  cache = {}
  def decorated_function(*args): 
    if args in cache:
      return cache[args]
    else:
      val = function(*args)
      cache[args] = val
      return val
  return decorated_function

def sc(A, S):
  """Measures the score of an NFA A and words S
  Input: an automaton A and the set of words S
  Output: a float"""

  @memoize
  def ch(i, w):
    """Calculates the size of encoding of the path
    followed to parse word w from the ith state in A
    Input: state's index, word
    Output: a float"""
    if w == '':
      return log(t[i], 2) if i in A.Final else float('inf')
    else:
      if i in A.delta and w[0] in A.delta[i]:
        return log(t[i], 2) + min(ch(j, w[1:]) for j in A.delta[i][w[0]])
      else:
        return float('inf')

  s = list(A.Initial)[0]
  t = dict()
  for i in xrange(len(A.States)):
    t[i] = 1 if i in A.Final else 0
    if i in A.delta:
      t[i] += sum(map(len, A.delta[i].itervalues()))
  return len(A.States) + sum(ch(s, w) for w in S) \
    + A.countTransitions()*(2*log(len(A.States), 2) \
    + log(len(A.Sigma), 2))

def synthesize(S):
  """Finds a consistent NFA by means of the MDL principle
  Input: set of positive words
  Output: an NFA"""
  A = buildPTA(S).toNFA()
  Red = {''}
  Blue = set(A.States)
  Blue.remove('')
  current_score = sc(A, S)
  while Blue:
    b = ql(Blue)[0]
    Blue.remove(b)
    for r in ql(Red):
      M = A.dup()
      merge(M.States.index(r), M.States.index(b), M)
      new_score = sc(M, S)
      if new_score < current_score:
        A = M
        current_score = new_score
        break
    if b in A.States:
      Red.add(b)
  return A
