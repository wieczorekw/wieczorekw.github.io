# Have to be invoked with ipy.exe -X:Frames, because of using networkx package
import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import *
sys.path.append(r"..\Ch3")
from Preliminaries3 import Parser
import networkx as nx
from networkx.algorithms.approximation.clique import max_clique
from itertools import combinations
from operator import add

def buildCharacteristicGraph(X):
  """Builds the characteristic graph of a given language
  Input: set of strings, X
  Output: an networkx undirected graph"""
  V = dict((x, set()) for x in X)
  G = nx.Graph()
  for x in X:
    for i in xrange(1, len(x)):
      V[x].add((x[:i], x[i:]))
      G.add_node((x[:i], x[i:]))
  for (u, w) in combinations(G.nodes_iter(), 2):
    if u[0] + u[1] != w[0] + w[1] and u[0] + w[1] in X and w[0] + u[1] in X:
      G.add_edge(u, w)
  return G

def split(X):
  """Finds a split for a given language without the empty string 
  nor words of length 1
  Input: a set of strings, X, epsilon not in X, and X is not 
  the subset of Sigma
  Output: sets A, B, C for which AB + C = X and A, B are 
  nontrivial"""
  G = buildCharacteristicGraph(X)
  K = max_clique(G)
  A = frozenset(u for (u, w) in K)  
  B = frozenset(w for (u, w) in K)
  C = frozenset(X - catenate(A, B))
  return (A, B, C)

def initialG(X, V, P, T, idx):
  """Builds initial grammar (via V and P) for finite language X
  Input: a set of strings (without the empty string), X, 
  references to an association table---variables V, productions P, 
  an alphabet T, and consecutive index 
  Output: an index for X (V, P, and idx are updated)"""
  i = idx[0]
  idx[0] += 1
  V[X] = i
  symbols = X & T
  if symbols:
    for s in symbols:
      P.add((i, s))
    X = X - symbols
  if X:
    A, B, C = split(X)
    a = V[A] if A in V else initialG(A, V, P, T, idx)
    b = V[B] if B in V else initialG(B, V, P, T, idx)
    P.add((i, a, b))
    if C:
      c = V[C] if C in V else initialG(C, V, P, T, idx)
      P.add((i, c))
  return i

def merge(i, j, P):
  """Joins two variables, i.e., V_j is absorbed by V_i
  Input: i, j variable indexes and grammar's productions P
  Output: a new production set, in which i and j have been 
  merged into i"""
  Q = set()
  for p in P:
    Q.add(tuple(i if x == j else x for x in p))
  return Q
  
def eliminateUnitProductions(P):
  """Eliminates productions of the form A -> B (A, B in nonterminals)
  Input: the set of productions (tuples)
  Output: the set of productions without unit productions"""
  Q = set(filter(lambda p: len(p) == 3 or isinstance(p[1], str), P))
  U = P - Q
  if U:
    D = nx.DiGraph(list(U))
    paths = nx.shortest_path_length(D)
    V = set(reduce(add, U))
    for (a, b) in combinations(V, 2):
      if b in paths[a]:
        for p in P:
          if p[0] == b and (len(p) == 3 or isinstance(p[1], str)):
            Q.add((a,) + p[1:])
      if a in paths[b]:
        for p in P:
          if p[0] == a and (len(p) == 3 or isinstance(p[1], str)):
            Q.add((b,) + p[1:])
  return Q

def makeCandidateVariablesList(V):
  """Builds the sorted list of pairs of variables to merge
  Input: a dictionary of variables, V
  Output: a list of pairs of variables' indexes, 
  first most promising"""
  card = dict()
  pairs = []
  for (I, i) in V.iteritems():
    for (J, j) in V.iteritems():
      if i < j:
        card[i, j] = len(I & J)
        pairs.append((i, j))
  pairs.sort(key = lambda x: -card[x])
  return pairs

def simplifiedGrammar(P, S):
  """Removes unnecessary productions
  Input: the set of productions, S_plus
  Output: the updated set of productions"""
  if len(P) > 1:
    cpy = list(P)
    for prod in cpy:
      P.remove(prod)
      parser = Parser(P)
      if not all(parser.accepts(w) for w in S):
        P.add(prod)
  return P

def synthesize(S_plus, S_minus):
  """Infers a CFG consistent with the sample
  Input: the sets of examples and counter-examples 
  (without the empty string)
  Output: a CFG in CNF"""
  V = dict()
  P = set() 
  T = alphabet(S_plus)
  idx = [0]
  initialG(frozenset(S_plus), V, P, T, idx)
  P = eliminateUnitProductions(P)
  joined = True
  while joined:
    pairs = makeCandidateVariablesList(V)
    joined = False
    for (i, j) in pairs:
      Q = merge(i, j, P)
      parser = Parser(Q)
      if not any(parser.accepts(w) for w in S_minus):
        P = Q
        for (key, val) in V.iteritems():
          if val == i: I = key
          if val == j: J = key
        del V[I]
        del V[J]
        V[I | J] = i
        joined = True
        break
  return simplifiedGrammar(P, S_plus)
