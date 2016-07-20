import os
import re
import time
import networkx
import sys
import random
from qgnfparser import *
from clique import mClique
from nslice import nth_cross_section

RUNS = 4
MAXLEN = 10
DLEN = 7
el = 1

def catenation(U, Y):
  X = set()
  for u in U:
    for y in Y:
      X.add(u+y)
  return X

def dobra_gramatyka(Produkcje):
  global Iks, Sigma
  n = len(Iks)
  Slowa = nth_cross_section(Produkcje, Sigma)
  n = len(Iks)
  for i in xrange(1, n):
    if Iks[i] != Slowa(i):
      return False
  return True
  
def podzial_z_kliki(k):
  L = set()
  P = set()
  for (a, b) in k:
    L.add(a)
    P.add(b)
  return (frozenset(L), frozenset(P))

def make_graph(X):
  V = []
  G = networkx.Graph()
  for x in X:
    for i in xrange(1, len(x)):
      V.append((x[:i], x[i:]))
      G.add_node((x[:i], x[i:]))
  for i in xrange(len(V)-1):
    for j in xrange(i+1, len(V)):
      if (V[i][0] + V[j][1] in X) and (V[j][0] + V[i][1] in X):
        G.add_edge(V[i], V[j])
  return G

def select_vertex(G, Y):
  tab = [(u, w) for (u, w) in G.nodes() if u+w not in Y]
  return random.choice(tab)

def is_a_clique(G):
  n = len(G)
  for (v, d) in G.degree_iter():
    if d < n-1:
      return False
  return True

def cover(X):
  G = make_graph(X)
  Y = set()
  size_of_X = len(X)
  while len(Y) < size_of_X:
    H = G.copy()
    (u, w) = select_vertex(H, Y)
    N = set(H.nodes())
    N = N - set(H.neighbors((u, w)) + [(u, w)])
    H.remove_nodes_from(N)
    if is_a_clique(H):
      K = set(H.nodes())
    else:
      K = mClique(H)
    (A, B) = podzial_z_kliki(K)
    C = catenation(A, B)
    for x in C:
      Y.add(x)
    yield (A, B)

def lq(w, X):
  U = set()
  l = len(w)
  for x in X:
    if x[:l] == w:
      U.add(x[l:])
  if w in X:
    U.add("")
  return U
  
def set_of_prefixes(l, X):
  U = set()
  for x in X:
    if len(x) >= l:
      U.add(x[:l])
  return U

def set_of_prefixes2(l, X):
  U = set()
  for x in X:
    if len(x) >= l:
      U.add(x[:l])
    else:
      U.add(x)
  return U

def rules(X):
  global P, V, nr, el, Sigma
  ix = nr[0]
  V[X] = ix
  nr[0] += 1
  for u in set_of_prefixes2(el, X):
    if len(u) < el:
      P.add((ix, u))
    else:
      A = lq(u, X)
      if "" in A:
        P.add((ix, u))
        A -= set([""])
      B = frozenset(A & Sigma)
      if len(B) > 0:
        vb = V[B] if B in V else rules(B)
        P.add((ix, (u, vb)))
      A -= B
      if len(A) > 0:
        for (C, D) in cover(A):
          vc = V[C] if C in V else rules(C)
          vd = V[D] if D in V else rules(D)
          P.add((ix, (u, vc, vd)))
  return ix

def Phase1():
  global X
  rules(X)

def Phase2():
  global P, V
  n = len(V)
  tab = range(n)
  for (zi, ni) in V.iteritems():
    tab[ni] = zi
  for i in xrange(n-1):
    for j in xrange(i+1, n):
      if tab[i] and tab[j]:
        P2 = set()
        for (A, alfa) in P:
          if A == j: A = i
          if isinstance(alfa, tuple) and len(alfa) == 3:
            (lan, B, C) = alfa
            if B == j: B = i
            if C == j: C = i
            P2.add((A, (lan, B, C)))
          elif isinstance(alfa, tuple) and len(alfa) == 2:
            (lan, B) = alfa
            if B == j: B = i
            P2.add((A, (lan, B)))
          else:
            P2.add((A, alfa))
        if dobra_gramatyka(P2):
          tab[j] = None
          P = P2

def allWords(A, n):
  Li = {""}
  for i in xrange(n):
    Li = {a+s for a in A for s in Li}
    for w in Li:
      yield w

def evaluateGrammar(G, Spos, Sneg):
  parser = Parser(G)
  unamb = True
  for w in Spos:
    r = parser.accepts(w)
    if r == 0:
      return False
    if r > 1:
      unamb = False
  for w in Sneg:
    r = parser.accepts(w)
    if r >= 1:
      return False
  return 'u' if unamb else 'a'      
  
sys.setrecursionlimit(10000)
random.seed()
tree = os.walk(".")
for katalog in tree:
  if katalog[0] == r".\jezyki":
    numery_jezykow = map(lambda nazwa: int(nazwa[1:-3]), katalog[2])
print "Nr".ljust(7), "Min t".ljust(7), "Max t".ljust(7), "Avg t".ljust(7),
print "Min P".ljust(7), "Max P".ljust(7), "Avg P".ljust(7),
print "Min V".ljust(7), "Max V".ljust(7), "Avg V".ljust(7),
print "#c".ljust(7), "#u".ljust(7), "#a".ljust(7)
for nr_jezyka in numery_jezykow:
  execfile(r".\jezyki" + r"\L" + str(nr_jezyka) + ".py")
  Spos, Sneg = set(), set()
  for w in allWords(Sigma, MAXLEN):
    if dobre(w):
      Spos.add(w)
    else:
      Sneg.add(w)
  X = frozenset(w for w in Spos if len(w) <= DLEN)
  Iks = [set() for i in xrange(DLEN + 1)]
  for x in X:
    Iks[len(x)].add(x)
  Sigma = set(Sigma)
  Time, lenP, lenV, Hashc, Hashu, Hasha = [], [], [], [], [], []
  for run in xrange(RUNS):
    czas_start = time.clock()
    P = set()
    V = {}
    nr = [0]
    Phase1()
    Phase2()
    czas_stop = time.clock()
    Time.append(czas_stop - czas_start)
    lenP.append(len(P))
    lenV.append(len(V))
    goodG = evaluateGrammar(P, Spos, Sneg)
    if goodG:
      Hashc.append(1)
      if goodG == 'u':
        Hashu.append(1)
        Hasha.append(0)
      elif goodG == 'a':
        Hashu.append(0)
        Hasha.append(1)
    else:
      Hashc.append(0)
      Hashu.append(0)
      Hasha.append(0)
  print str(nr_jezyka).ljust(7),
  print ("%5.2f  " % min(Time)),
  print ("%5.2f  " % max(Time)),
  print ("%5.2f  " % (sum(Time)/RUNS)),
  print str(min(lenP)).ljust(7),
  print str(max(lenP)).ljust(7),
  print ("%5.1f  " % (float(sum(lenP))/RUNS)),
  print str(min(lenV)).ljust(7),
  print str(max(lenV)).ljust(7),
  print ("%5.1f  " % (float(sum(lenV))/RUNS)),
  print str(sum(Hashc)).ljust(7),
  print str(sum(Hashu)).ljust(7),
  print str(sum(Hasha)).ljust(7)
