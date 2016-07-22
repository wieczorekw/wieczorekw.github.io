def cat(U, Y):
  X = set()
  for u in U:
    for y in Y:
      X.add(u+y)
  return X

def comps(n, d1, d2):
  if d2 == 0:
    if d1 == n:
      yield d1*[1]
  elif d2 == 1:
    if n > d1:
      yield (d1*[1]) + [n-d1]
  else:
    if n > d1+1:
      for i in xrange(1, n-d1):
        yield (d1*[1]) + [i] + [n-d1-i] 

class nth_cross_section(object):

  def __init__(self, P, alfabet):
    self.terms = list(alfabet)
    self.prods = {}
    for (lewa, prawa) in P:
      if lewa in self.prods:
        self.prods[lewa].append(prawa)
      else:
        self.prods[lewa] = [prawa]
    self.nonts = self.prods.keys()
    self.tab = {}
    for s in self.terms + self.nonts:
      self.tab[(s, 1)] = self.ell(self.tab, s, 1)
    self.n = 1

  def pvars(self, v):
    if v in self.prods:
      return self.prods[v]
    else:
      return []

  def ell(self, mapa, symbol, liczba):
    if symbol in self.terms:
      return set([symbol]) if liczba == 1 else set([])
    else:
      unions = set()
      for p in self.pvars(symbol):
        unions.update(self.app(mapa, liczba, p))
      return unions

  def app(self, mapa, n, p):
    if isinstance(p, tuple):
      seq = list(p[0]) + list(p[1:])
      d1, d2 = len(p[0]), len(p[1:])
    else:
      seq = list(p)
      d1, d2 = len(p), 0
    unions = set()
    for tab in comps(n, d1, d2):
      derive = set([""])
      for st in zip(seq, tab):
        derive = cat(derive, mapa[st])
      unions.update(derive)
    return unions

  def __call__(self, j):
    if j > self.n:
      for i in xrange(self.n+1, j+1):
        for s in self.nonts:
          self.tab[(s, i)] = self.ell(self.tab, s, i)
      self.n = j
    return self.tab[(0, j)]

