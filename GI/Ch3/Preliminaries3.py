from FAdo.fa import *

class Parser(object):
  """A parser class for CNF grammars"""
  
  def __init__(self, productions):
    self.__prods = productions
    self.__cache = dict()
    
  def __parse(self, w, var):
    """Unger's parsing method
    Input: a word, a non-terminal (an integer)
    Output: true or false"""
    if (w, var) in self.__cache:
      return self.__cache[w, var]
    else:
      n = len(w)
      if n == 1: return (var, w) in self.__prods
      for p in self.__prods:
        if p[0] == var:
          if len(p) == 3:
            for i in xrange(1, n):
              if self.__parse(w[:i], p[1]) \
                and self.__parse(w[i:], p[2]):
                self.__cache[w, var] = True
                return True
      self.__cache[w, var] = False
      return False
      
  def accepts(self, word):
    """Membership query
    Input: a string
    Output: true or false"""
    self.__cache.clear()
    return self.__parse(word, 0)
    
  def grammar(self):
    return self.__prods
    
def inducedNFA(P, A):
  """Join groups of states for a new automaton
  Input: the partition P (the list of frozensets) and an NFA A
  Output: a new NFA, A/P"""
  B = NFA()
  d = dict()
  K = range(len(A.States))
  for p in P:
    d[p] = j = B.addState(p)
    if p & A.Initial:
      B.addInitial(j)
    if p & A.Final:
      B.addFinal(j)
    for state in p:
      K[state] = j
  for q in A.delta:
    for a in A.delta[q]:
      for r in A.delta[q][a]:
        B.addTransition(K[q], a, K[r])
  return B

def inducedCFG(P, G):
  """Join groups of variables for a new CFG
  Input: a sorted partition P and productions G in CNF
  Output: a new CFG in Chomsky normal form, G/P"""
  K = dict((v, i) for i in xrange(len(P)) for v in P[i])
  Pprime = set()
  for p in G:
    if len(p) == 3:
      (A, B, C) = p
      Pprime.add((K[A], K[B], K[C]))
    elif isinstance(p[1], str):
      (A, a) = p
      Pprime.add((K[A], a))
  return Pprime
