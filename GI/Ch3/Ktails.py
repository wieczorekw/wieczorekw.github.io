import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import accepts, buildPTA, suffixes
from Preliminaries3 import inducedNFA

def synthesize(X):
  """Finds NFAs for k = 0, 1, ... by means of the k-tails method
  Input: the set of strings
  Output: an iterator over NFAs"""
  minanfa = buildPTA(X).minimalHopcroft().toNFA()
  n = len(minanfa.States)
  m = max(len(x) for x in X)
  S = suffixes(X)
  langs = []
  for i in xrange(n):
    langs.append(set(w for w in S if accepts(w, i, minanfa)))
  for k in xrange(m):
    d = dict()
    for i in xrange(n):
      el = frozenset(w for w in langs[i] if len(w) <= k)
      if el in d:
        d[el].add(i)
      else:
        d[el] = {i}
    partition = map(frozenset, d.itervalues())
    yield inducedNFA(partition, minanfa)