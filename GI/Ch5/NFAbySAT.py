import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import *
from satispy import Variable
from satispy.solver import Minisat
from operator import and_, or_

class Idx(object):
  def __init__(self, start):
    self.__counter = start
  def __add__(self, step):
    self.__counter += step
    return self.__counter
  
def encode(Sp, Sm, k):
  """Write NFA induction as SAT
  Input: examples, counter-examples, and an integer
  Output: boolean formula (Cnf), variables y and z"""
  idx = Idx(0)
  Sigma = alphabet(Sp | Sm)
  Q = range(k)
  P = prefixes(Sp | Sm)
  P.remove("")
  x = dict(((w, q), Variable(idx + 1)) for w in P for q in Q)
  y = dict(((a, p, q), Variable(idx + 1)) for a in Sigma for p in Q for q in Q)
  z = dict((q, Variable(idx + 1)) for q in Q)
  st = [] # subject to (i.e. constraints)
  
  # The empty word inclusion
  if "" in Sp: st.append(z[0])
  if "" in Sm: st.append(-z[0])
  
  # Acceptance of examples
  for w in Sp - {""}:
    st.append(reduce(or_, (x[w, q] & z[q] for q in Q)))
  
  # Rejection of counter-examples
  for w in Sm - {""}:
    for q in Q:
      st.append(-x[w, q] | -z[q])
  
  # Single-symbol prefixes inclusion
  for a in P & Sigma:
    for q in Q:
      st.append(-(x[a, q] ^ y[a, 0, q]))

  # Multi-symbol prefixes inclusion
  for w in P:
    if len(w) >= 2:
      v, a = w[:-1], w[-1]
      for q in Q:
        st.append(x[w, q] >> reduce(or_, (x[v, r] & y[a, r, q] for r in Q)))
        for r in Q:
          st.append((x[v, r] & y[a, r, q]) >> x[w, q])
        
  return (reduce(and_, st), y, z)
  
def decode(solution, y, z, k):
  """Constructs an NFA from the values of y, x and k > 0
  Input: satispy Solution and Variables
  Output: a k-state NFA"""
  A = NFA()
  for i in xrange(k):
    A.addState()
  A.addInitial(0)
  for q in xrange(k):
    if solution[z[q]]:
      A.addFinal(q)
  for ((a, p, q), var) in y.iteritems():
    if solution[var]:
      A.addTransition(p, a, q)
  return A

def synthesize(S_plus, S_minus, k):
  """Infers an NFA A consistent with the sample
  Input: the sets of examples and counter-examples, k > 0
  Output: a k-states NFA or None"""
  formula, y, z = encode(S_plus, S_minus, k)
  solver = Minisat()
  sol = solver.solve(formula)
  return decode(sol, y, z, k) if sol.success else None
