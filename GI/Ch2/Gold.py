from Preliminaries2 import *

def buildTable(S_plus, S_minus):
  """Builds an initial observation table
  Input: a sample
  Output: OT as dictionary and sets: Red, Blue, EXP"""
  OT = dict()
  EXP = suffixes(S_plus | S_minus)
  Red = {''}
  Blue = alphabet(S_plus | S_minus)
  for p in Red | Blue:
    for e in EXP:
      if p+e in S_plus:
        OT[p, e] = 1
      else:
        OT[p, e] = 0 if p+e in S_minus else '*'
  return (Red, Blue, EXP, OT)

def buildAutomaton(Red, Blue, EXP, OT):
  """Builds a DFA from closed and complete observation table
  Input: raws (Red + Blue), columns (EXP), and table (OT)
  Output: a DFA"""
  A = DFA()
  A.setSigma(alphabet(Red | Blue | EXP))
  q = dict()
  for r in Red:
    q[r] = A.addState(r)
  for w in Red | Blue:
    for e in EXP:
      if w+e in Red and OT[w, e] == 1:
        A.addFinal(q[w+e])
  for w in iter(q):
    for u in iter(q):
      for a in A.Sigma:
        if all(OT[u, e] == OT[w+a, e] for e in EXP):
          A.addTransition(q[w], a, q[u])
  A.setInitial(q[''])
  return A

def fillHoles(Red, Blue, EXP, OT):
  """Tries to fill in holes in OT
  Input: raws (Red + Blue), columns (EXP), and table (OT)
  Output: true if success or false if fail"""
  for b in ql(Blue):
    found = False
    for r in ql(Red):
      if not any(OT[r, e] == 0 and OT[b, e] == 1 \
        or OT[r, e] == 1 and OT[b, e] == 0 for e in EXP):
        found = True
        for e in EXP:
          if OT[b, e] != '*':
            OT[r, e] = OT[b, e]
    if not found:
      return False
  for r in Red:
    for e in EXP:
      if OT[r, e] == '*':
        OT[r, e] = 1
  for b in ql(Blue):
    found = False
    for r in ql(Red):
      if not any(OT[r, e] == 0 and OT[b, e] == 1 \
        or OT[r, e] == 1 and OT[b, e] == 0 for e in EXP):
        found = True
        for e in EXP:
          if OT[b, e] == '*':
            OT[b, e] = OT[r, e]
    if not found:
      return False
  return True

def OD(u, v, EXP, OT):
  """Checks if raws u and v obviously different for OT
  Input: two raws (prefixes), columns, and table
  Output: boolean answer"""
  return any(OT[u, e] in {0, 1} and OT[v, e] in {0, 1} \
    and OT[u, e] != OT[v, e] for e in EXP)

def synthesize(S_plus, S_minus):
  """Infers a DFA consistent with the sample
  Input: the sets of examples and counter-examples
  Output: a DFA"""
  (Red, Blue, EXP, OT) = buildTable(S_plus, S_minus)
  Sigma = alphabet(S_plus | S_minus)
  x = ql(b for b in Blue if all(OD(b, r, EXP, OT) for r in Red))
  while x:
    Red.add(x[0])
    Blue.discard(x[0])
    Blue.update(catenate({x[0]}, Sigma))
    for u in Blue:
      for e in EXP:
        if u+e in S_plus:
          OT[u, e] = 1
        else:
          OT[u, e] = 0 if u+e in S_minus else '*'
    x = ql(b for b in Blue if all(OD(b, r, EXP, OT) for r in Red))
  if not fillHoles(Red, Blue, EXP, OT):
    return buildPTA(S_plus)
  else:
    A = buildAutomaton(Red, Blue, EXP, OT)
    if all(A.evalWordP(w) for w in S_plus) \
      and not any(A.evalWordP(w) for w in S_minus):
      return A
    else:
      return buildPTA(S_plus)
