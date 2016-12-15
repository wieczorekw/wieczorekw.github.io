# Have to be invoked with ipy.exe -X:Frames, because of using networkx package
import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import alphabet, prefixes
from itertools import count
import networkx as nx

class DAWG(object):
  """A class for storing DAWGs for the GI algorithm"""
  
  def __init__(self, Sp):
    """Constructs an initial DAWG from given words
    Input: the set of strings (not containing the empty word)
    Output: this object becomes the initial DAWG"""

    def lq(w, X):
      n = len(w)
      U = set()
      for x in X:
        if x[:n] == w:
          U.add(x[n:])
      return frozenset(U)
      
    def isArc(a, u, v):
      if v == {''}:
        return a in u
      for x in u:
        if x != '' and x[0] == a and x[1:] not in v:
          return False
      for x in v:
        if a+x not in u:
          return False
      return True

    self.__Sigma = alphabet(Sp)
    P = prefixes(Sp)
    V = dict(zip(set(lq(w, Sp) for w in P), count(0)))
    self.__s = V[frozenset(Sp)]
    self.__t = V[frozenset({''})]
    self.__ell = dict()
    for a in self.__Sigma:
      for u in V:
        for v in V:
          if isArc(a, u, v):
            ind = (V[u], V[v])
            if ind in self.__ell:
              self.__ell[ind].add(a)
            else:
              self.__ell[ind] = {a}
            
  def accepts(self, word):
    """Checks whether given word is stored in this DAWG
    Input: a string
    Output: True or False"""
  
    def delta(q, w):
      if (q, w) in cache:
        return cache[q, w]
      else:
        if w == "" and q == self.__t:
          cache[q, w] = True
          return True
        elif w == "" and q != self.__t:
          cache[q, w] = False
          return False
        else:
          for (u, v) in self.__ell:
            if u == q and w[0] in self.__ell[u, v]:
              if delta(v, w[1:]):
                cache[q, w] = True
                return True
          cache[q, w] = False
          return False
        
    cache = dict()
    return delta(self.__s, word)   
    
  def __findPotencyList(self):
    """Finds a potency for every arc
    Input: this object
    Output: sorted arcs according to decreasing potencies"""
    D = nx.DiGraph(self.__ell.iterkeys())
    res = dict()
    for (u, v) in self.__ell.iterkeys():
      if v == self.__t:
        res[u, v] = 1
      else:
        res[u, v] = len(list( \
          nx.all_simple_paths(D, source=v, target=self.__t)))
    return list(reversed(sorted(res, key=res.__getitem__)))

  def extend(self, Sm):
    """The second phase of the GI algorithm
    Input: the set of counter-examples
    Output: this DAWG is updated"""
    A = self.__findPotencyList()
    for (u, v) in A:
      for a in self.__Sigma:
        if a not in self.__ell[u, v]: 
          self.__ell[u, v].add(a)
          if any(self.accepts(w) for w in Sm):
            self.__ell[u, v].remove(a)
