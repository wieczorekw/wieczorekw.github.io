import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import catenate

class Structure(object):
  """The class for storing hypotheses of Alignment-Based
  Learning"""
  
  def __init__(self, seq):
    """Structure is a list of sets (of strings)
    and strings"""
    self.__sequence = seq
    
  def __eq__(self, ob):
    if len(self.__sequence) != len(ob.__sequence):
      return False
    for (a, b) in zip(self.__sequence, ob.__sequence):
      if type(a) != type(b):
        return False
      if isinstance(a, str) and (a != b):
        return False
    return True
    
  def __nonzero__(self):
    return self.__sequence != []

  def update(self, ob):
    """Adds new constituents to this structure
    Input: another compatible structure
    Output: an updated structure"""
    for (a, b) in zip(self.__sequence, ob.__sequence):
      if isinstance(a, set):
        a.update(b)
        
  def size(self):
    """Returns the number of words represented by this structure"""
    result = 1
    for el in self.__sequence:
      if isinstance(el, set):
        result *= len(el)
    return result
    
  def words(self):
    """Returns the set of words represented by this structure"""
    return reduce(catenate, map( \
      lambda x: {x} if isinstance(x, str) else x, 
        self.__sequence))

def lcs(x, y):
  """Finds an lcs of two strings"""
  n = len(x)
  m = len(y)
  table = dict() 
  for i in xrange(n+1): 
    for j in xrange(m+1):
      if i == 0 or j == 0:
        table[i, j] = 0
      elif x[i-1] == y[j-1]:
        table[i, j] = table[i-1, j-1] + 1
      else:
        table[i, j] = max(table[i-1, j], table[i, j-1])

  def recon(i, j):
    if i == 0 or j == 0:
      return ""
    elif x[i-1] == y[j-1]:
      return recon(i-1, j-1) + x[i-1]
    elif table[i-1, j] > table[i, j-1]:
      return recon(i-1, j)
    else:
      return recon(i, j-1)

  return recon(n, m)

def align(x, y):
  """Finds the identical and distinct parts between two words
  Input: two strings
  Output: an instance of the Structure class"""
  seq = []
  same = lcs(x, y)
  i2, n = 0, len(same)
  ix, iy = 0, 0
  while i2 < n:
    wx, wy = "", ""
    i1 = i2
    while x[ix] != same[i1]:
      wx += x[ix]
      ix += 1
    while y[iy] != same[i1]:
      wy += y[iy]
      iy += 1
    while i2 < n and x[ix] == y[iy] == same[i2]:
      i2 += 1
      ix += 1
      iy += 1
    seq.append({wx, wy})
    seq.append(same[i1:i2])
  if same: seq.append({x[ix:], y[iy:]})
  return Structure(seq)

def synthesize(S):
  """Finds a set of structures that covers S
  Input: a list of words
  Output: a list of structures"""
  n = len(S)
  hypotheses = []
  for i in xrange(n-1):
    for j in xrange(i+1, n):
      s = align(S[i], S[j])
      if s:
        k, m = 0, len(hypotheses)
        while k < m:
          if s == hypotheses[k]:
            hypotheses[k].update(s)
            break
          k += 1
        if k == m:
          hypotheses.append(s)
  hypotheses.sort(key = lambda x: -x.size())
  Sp = set(S)
  X = hypotheses[0].words()
  idx = 1
  while not (Sp <= X):
    X.update(hypotheses[idx].words())
    idx += 1
  return hypotheses[:idx]
