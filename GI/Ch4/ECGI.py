from FAdo.fa import *

infinity = (float('inf'), ())

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

@memoize
def C(q, x, A):
  """Determine optimal error-correcting path
  Input: a state, a word, and an acyclic NFA
  Output: (rank, (q_0, e_0, p_1, e_1, ..., q_1))"""
  if x != "" and q not in A.Final:
    return min( \
      (1 + C(q, x[1:], A)[0], (q, 'i' + x[0]) + C(q, x[1:], A)[1]), \
      min( (C(r, x[1:], A)[0], (q, x[0]) + C(r, x[1:], A)[1]) \
      for r in A.delta[q][x[0]] ) if x[0] in A.delta[q] else infinity, \
      min( (1 + C(r, x[1:], A)[0], (q, 's' + x[0]) + C(r, x[1:], A)[1]) \
      for b in A.delta[q] for r in A.delta[q][b] ), \
      min( (1 + C(r, x, A)[0], (q, 'd' + b) + C(r, x, A)[1]) \
      for b in A.delta[q] for r in A.delta[q][b] ) )
  if x == "" and q not in A.Final:
    return infinity
  if x != "" and q in A.Final:
    return infinity
  if x == "" and q in A.Final:
    return (0, (q,))

def addPath(word, start, stop, A):
  """Inserts a word into an automaton between states start and stop
  Input: a string, two states, an acyclic NFA
  Output: an updated NFA"""
  i = start
  for c in word[:-1]:
    j = A.addState()
    A.addTransition(i, c, j)
    i = j
  A.addTransition(i, word[-1], stop)

def initial(a):
  """Builds an initial acyclic NFA
  Input: a word
  Output: an NFA"""
  A = NFA()
  init = A.addState()
  final = A.addState()
  A.addInitial(init)
  A.addFinal(final)
  addPath(a, init, final, A)
  return (A, init)

def synthesize(ListOfWords):
  """Synthesizes an acyclic NFA by means of the ECGI method
  Input: the list of example words
  Output: an NFA"""
  A, init = initial(ListOfWords[0])
  for idx in xrange(1, len(ListOfWords)):
    w = ListOfWords[idx]
    d = list(C(init, w, A)[1])
    n = len(d)
    i = 0
    while i < n-1:
      while i < n-1 and len(d[i+1]) == 1:
        i += 2
      j = i
      while j < n-1 and len(d[j+1]) == 2:
        j += 2
      if i < j:
        alpha = ""
        for k in xrange(i+1, j, 2):
          if d[k][0] != "d":
            alpha += d[k][1]
        if j < n-1:
          addPath(alpha + d[j+1], d[i], d[j+2], A)
        else:
          addPath(alpha, d[i], d[j], A)
        i = j+2
  return A
