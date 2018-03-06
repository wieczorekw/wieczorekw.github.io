# Have to be invoked with ipy.exe -X:Frames
import sys
sys.path.append(r"..\Ch6")
from CFGbyDecomposition import *
from itertools import count, izip
from operator import countOf

def synthesize(S_plus):
  V = dict()
  P = set()
  T = {"0", "1"}
  idx = [0]
  initialG(frozenset(S_plus), V, P, T, idx)
  return eliminateUnitProductions(P)

def i2str(i):
  """Makes the string representation of an implicant
  Input: An implicant i is represented as a tuple of integers from
  the set {0, 1, 3}.  The three means that there is no appropriate
  variable in a product, for example (1, 3, 0, 1) = A C' D.
  Output: a string (for example: A B' C D')"""
  sym = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  lst = []
  for (v, pos) in izip(i, count(0)):
    if v != 3:
      lst.append(sym[pos] + ("'" if v == 0 else ""))
  return " ".join(lst)

def allSentences(grammar, length):
  """Generates all sentential forms of a certain length
  that can be derived in a given grammar
  Input: a grammar (the set of tuples) and an integer
  Output: tuples of integers (each integer is a non-terminal)"""
  Z = {(0,)}
  sentences = set()
  visited = set()
  while Z:
    t = Z.pop()
    n = len(t)
    if n < length:
      for i in xrange(n):
        for p in grammar:
          if p[0] == t[i] and len(p) == 3:
            w = t[:i] + p[1:] + t[i+1:]
            if w not in visited:
              Z.add(w)
              visited.add(w)
    else:
      sentences.add(t)
  return sentences

def cfg2bf(g, n):
  """Converts a CFG to a boolean function with n variables
  Input: the set of tuples, an integer
  Output: a boolean function as string like this: A B' + C"""
  d = dict()  # for determining the kind of a non-terminal
  for p in g:
    if p[0] not in d:
      d[p[0]] = set()
    if len(p) == 2:
      d[p[0]].add(p[1])
  implicants = set()
  for s in allSentences(g, n):
    if all(v in d and d[v] for v in s):
      i = tuple(3 if d[v] == {'0', '1'} \
        else (1 if '1' in d[v] else 0) for v in s)
      implicants.add(i)
  sortkey = lambda i: countOf(i, 3)
  t = sorted(implicants, key=sortkey)
  ino = len(implicants)
  for j in xrange(ino-1):
    for k in xrange(j+1, ino):
      if all(a == 3 or a == b for (a, b) in zip(t[k], t[j])):
        implicants.remove(t[j])
        break
  return " + ".join(map(i2str, implicants))

X = {'0000110', '0000100', '0001100', '0001110', '0100000', '0100010', '0100100', '0100110', \
'0101000', '0101010', '0101100', '0101110', '1000100', '1000110', '1001100', '1001110', \
'0010100', '0010110', '0011100', '0011110', '0110000', '0110010', '0110100', '0110110', \
'0111000', '0111010', '0111100', '0111110', '1010100', '1010110', '1011100', '1011110', \
'0000101', '0000111', '0001101', '0001111', '0010101', '0010111', '0011101', '0011111', \
'0100001', '0100011', '0100101', '0100111', '0101001', '0101011', '0101101', '0101111', \
'0110001', '0110011', '0110101', '0110111', '0111001', '0111011', '0111101', '0111111', \
'1000101', '1000111', '1001101', '1001111', '1010101', '1010111', '1011101', '1011111'}
g = synthesize(X)
print g
f = cfg2bf(g, 7)
print "F =", f
