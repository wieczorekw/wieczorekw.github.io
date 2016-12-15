from Preliminaries3 import *
from pyevolve import G1DList
from pyevolve import GSimpleGA

class Idx(object):
  """A class for simple indexing
  Declaration: i = Idx(0)
  Usage: n = i+1 or fun(i+1)"""
  def __init__(self, start):
    self.__counter = start
  def __add__(self, step):
    self.__counter += step
    return self.__counter

def tr(w, idx):
  """Returns non-terminals of tabular representation for w
  Input: a string
  Output: the dictionary of non-terminals"""
  n = len(w)
  X = dict()
  for i in xrange(1, n+1):
    X[i, 1, 1] = idx+1
    for j in xrange(2, n-i+2):
      for k in xrange(1, j):
        X[i, j, k] = idx+1
  return X

def primitiveCFG(w, X):
  """Constructs the productions of a primitive CFG
  Input: a string w and nonterminals from a tabular 
         representation for w
  Output: the set of productions"""
  n = len(w)
  P = {(0, X[1, n, k]) for k in xrange(1, max(2, n))}
  for i in xrange(1, n+1):
    P.add((X[i, 1, 1], w[i-1]))
    for j in xrange(1, n-i+2):
      for k in xrange(1, j):
        for l1 in xrange(1, max(2, k)):
          for l2 in xrange(1, max(2, j-k)):
            P.add((X[i, j, k], X[i, k, l1], X[i+k, j-k, l2]))
  return P

def decodeToPi(chromosome):
  """Finds an appropriate partition (a block with 0 first)
  Input: a chromosome
  Output: a sorted partition as the list of frozensets"""
  t = dict()
  n = len(chromosome)
  for (v, i) in zip(chromosome, range(n)):
    if v in t:
      t[v].add(i)
    else:
      t[v] = {i}
  return sorted(map(frozenset, t.itervalues()), key=min)

posPart = set()
negPart = set()
GTU = set()  # G(T(U_+))

def eval_func(chromosome):
  """The fitness function
  Input: a chromosome
  Output: a float"""
  global posPart, negPart, GTU
  Pi = decodeToPi(chromosome)
  G = inducedCFG(Pi, GTU)
  parser = Parser(G)
  if any(parser.accepts(w) for w in negPart):
    return 0.0
  f1 = 0
  for w in posPart:
    if parser.accepts(w):
      f1 += 1
  if f1 == 0: return 0.0
  f1 /= float(len(posPart))
  f2 = float(len(chromosome)) / len(Pi)
  return f1 + f2

def synthesize(Uplus, Uminus):
  """Finds a CFG consistent with the input by means of GA
  Input: a sample, Sample = (Uplus, Uminus) without lambda
  Output: the parser of an inferred CFG or None"""
  global posPart, negPart, GTU
  posPart, negPart = Uplus, Uminus
  idx = Idx(0)
  GTU = set()
  for w in Uplus:
    GTU.update(primitiveCFG(w, tr(w, idx)))
  nvars = idx+1
  genome = G1DList.G1DList(nvars)
  genome.setParams(rangemin = 0, rangemax = nvars-1)
  genome.evaluator.set(eval_func)
  ga = GSimpleGA.GSimpleGA(genome)
  ga.setGenerations(400)
  ga.setCrossoverRate(0.9)
  ga.setMutationRate(0.05)
  ga.setPopulationSize(1000)
  ga.evolve(freq_stats=50)  # will show the statistics 
  # every 50th generation (the parameter may be omitted)
  best_indiv = ga.bestIndividual()
  Pi = decodeToPi(best_indiv)
  G = inducedCFG(Pi, GTU)
  parser = Parser(G)
  if any(parser.accepts(w) for w in Uminus) \
    or not all(parser.accepts(w) for w in Uplus):
    return None
  return parser 
