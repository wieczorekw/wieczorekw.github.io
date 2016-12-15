# Have to be invoked with ipy.exe -X:Frames, because of using networkx package
import networkx as nx
from pipetools import *

def pairFromClique(C):
  """Returns a SFRE induced by C
  Input: the list of nodes (every node is the pair of words)
  Output: the pair of sets of words"""
  U = set()
  W = set()
  for (a, b) in C:
    U.add(a)
    W.add(b)
  return (U, W)

def sfreFromCliques(cliques):
  """Finds a SFRE from cliques
  Input: an iterator over lists (cliques)
  Output: a SFRE as the list of pairs of sets of words"""
  result = []
  for C in cliques:
    (U, W) = pairFromClique(C)
    result.append((U, W))
  return result

def buildGraph(S):
  """Constructs a graph G
  Input: a sample - the pair of sets
  Output: an undirected networkx graph"""
  Sp, Sn = S[0], S[1]
  V = []
  G = nx.Graph()
  for x in Sp:
    for i in xrange(1, len(x)):
      V.append((x[:i], x[i:]))
      G.add_node((x[:i], x[i:]))
  for i in xrange(len(V) - 1):
    for j in xrange(i+1, len(V)):
      w1 = V[i][0] + V[j][1]
      w2 = V[j][0] + V[i][1]
      if (len(V[i][0]) == len(V[j][0])) \
        and (w1 not in Sn) and (w2 not in Sn):
        G.add_edge(V[i], V[j])
  return G

def accepts(e, x):
  """A membership query
  Input: a SFRE and a word
  Output: true or false"""
  for (p, s) in ((x[:i], x[i:]) for i in xrange(1, len(x))):
    for (L, R) in e:
      if p in L and s in R:
        return True
  return False

synthesize = (pipe
| buildGraph
| nx.find_cliques
| sfreFromCliques)
