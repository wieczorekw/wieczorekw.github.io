from FAdo.fa import *

def alphabet(S):
  """Finds all letters in S
  Input: a set of strings: S
  Output: the alphabet of S"""
  result = set()
  for s in S:
    for a in s:
      result.add(a)
  return result

def prefixes(S):
  """Finds all prefixes in S
  Input: a set of strings: S
  Output: the set of all prefixes of S"""
  result = set()
  for s in S:
    for i in xrange(len(s) + 1):
      result.add(s[:i])
  return result

def suffixes(S):
  """Finds all suffixes in S
  Input: a set of strings: S
  Output: the set of all suffixes of S"""
  result = set()
  for s in S:
    for i in xrange(len(s) + 1):
      result.add(s[i:])
  return result
  
def catenate(A, B):
  """Determine the concatenation of two sets of words
  Input: two sets (or lists) of strings: A, B
  Output: the set AB"""
  return set(a+b for a in A for b in B)

def ql(S):
   """Returns the list of S in quasi-lexicographic order
   Input: collection of strings
   Output: a sorted list"""
   return sorted(S, key = lambda x: (len(x), x))

def buildPTA(S):
  """Build a prefix tree acceptor from examples
  Input: the set of strings, S
  Output: a DFA representing PTA"""
  A = DFA()
  q = dict()
  for u in prefixes(S):
    q[u] = A.addState(u)
  for w in iter(q):
    u, a = w[:-1], w[-1:]
    if a != '':
      A.addTransition(q[u], a, q[w])
    if w in S:
      A.addFinal(q[w])
  A.setInitial(q[''])
  return A

def merge(q1, q2, A):
  """Join two states, i.e., q2 is absorbed by q1
  Input: q1, q2 state indexes and an NFA A
  Output: the NFA A updated"""
  n = len(A.States)
  for q in xrange(n):  
    if q in A.delta:
      for a in A.delta[q]:
        if q2 in A.delta[q][a]: A.addTransition(q, a, q1)
    if q2 in A.delta:
      for a in A.delta[q2]:
        if q in A.delta[q2][a]: A.addTransition(q1, a, q)
  if q2 in A.Initial: A.addInitial(q1)
  if q2 in A.Final: A.addFinal(q1)
  A.deleteStates([q2])
  return A

def accepts(w, q, A):
  """Verify if in an NFA A, a state q recognizes given word
  Input: a string w, a state index (int) q, and an NFA A
  Output: yes or no as Boolean value"""
  ilist = A.epsilonClosure(q)
  for c in w:
    ilist = A.evalSymbol(ilist, c)
    if not ilist:
      return False
  return not A.Final.isdisjoint(ilist)
