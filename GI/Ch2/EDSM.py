from Preliminaries2 import *

def makeCandidateStatesList(U, A):
  """Build the sorted list of pairs of states to merge
  Input: a set of suffixes, U, and an NFA, A
  Output: a list of pairs of states, first most promising"""
  n = len(A.States)
  score = dict()
  langs = []
  pairs = []
  for i in xrange(n):
    langs.append(set(u for u in U if accepts(u, i, A)))
  for i in xrange(n-1):
    for j in xrange(i+1, n):
      score[i, j] = len(langs[i] & langs[j])
      pairs.append((i, j))
  pairs.sort(key = lambda x: -score[x])
  return pairs
  
def synthesize(S_plus, S_minus):
  """Infers an NFA consistent with the sample
  Input: the sets of examples and counter-examples
  Output: an NFA"""
  A = buildPTA(S_plus).toNFA()
  U = suffixes(S_plus)
  joined = True
  while joined:
    pairs = makeCandidateStatesList(U, A)
    joined = False
    for (p, q) in pairs:
      B = A.dup()
      merge(p, q, B)
      if not any(B.evalWordP(w) for w in S_minus):
        A = B
        joined = True
        break
  return A