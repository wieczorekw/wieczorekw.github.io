import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import *
from Preliminaries3 import *
from FAdo.fa import *
from FAdo.common import DFAsymbolUnknown
from itertools import izip, count
from pyevolve import Consts
from pyevolve import G1DList
from pyevolve import GSimpleGA

negPart = []
PTA = NFA()

def incrementalInference(S_plus, S_minus, f_syn, elem):
  """Semi-incremental procedure for GI
  Input: a sample, a synthesizing function, and a membership
         query function
  Output: an NFA consistent with S or None"""
  Sp, Sm = ql(S_plus), ql(S_minus)
  n = len(S_plus)
  j = 2  
  I = Sp[0:j]
  while j <= n:
    hypothesis = f_syn(I, Sm)
    k = j
    if hypothesis:
      while k < n:
        if elem(Sp[k], hypothesis): k += 1
        else: break
    if k < n: I.append(Sp[k])
    else: break
    j = k+1
  return hypothesis

def decodeToPi(chromosome):
  """Finds an appropriate partition
  Input: a chromosome
  Output: a partition as the list of frozensets"""
  t = dict()
  for (v, i) in izip(chromosome, count(0)):
    if v in t:
      t[v].add(i)
    else:
      t[v] = {i}
  return map(frozenset, t.itervalues())

def accepted(word, automaton):
  """Checks whether a word is accepted by an automaton
  Input: a string and an NFA
  Output: true or false"""
  try:
    return automaton.evalWordP(word)
  except DFAsymbolUnknown:
    return False

def eval_func(chromosome):
  """The fitness function
  Input: a chromosome
  Output: a float"""
  global negPart, PTA
  Pi = decodeToPi(chromosome)
  A = inducedNFA(Pi, PTA)
  if any(accepted(w, A) for w in negPart):
    return float('infinity')
  else:
    return len(Pi)

def synthesizeByGA(positives, negatives):
  """Finds an NFA consistent with the input by means of GA
  Input: a sample, S = (positives, negatives)
  Output: an NFA or None"""
  global negPart, PTA
  negPart = negatives
  PTA = buildPTA(positives).toNFA()
  genome = G1DList.G1DList(len(PTA.States))
  genome.setParams(rangemin=0, rangemax=len(PTA.States)-1)
  genome.evaluator.set(eval_func)
  ga = GSimpleGA.GSimpleGA(genome)
  ga.setGenerations(500)
  ga.setMinimax(Consts.minimaxType["minimize"])
  ga.setCrossoverRate(0.9)
  ga.setMutationRate(0.05)
  ga.setPopulationSize(200)
  ga.evolve()
  best_indiv = ga.bestIndividual()
  if best_indiv.getRawScore() == float('infinity'):
    return None
  else:
    Pi = decodeToPi(best_indiv)
    A = inducedNFA(Pi, PTA)
    return A

def synthesize(S_plus, S_minus):
  """Finds an NFA consistent with the input by means of GA
  using incremental procedure
  Input: a sample, S = (S_plus, S_minus), |S_plus| > 1
  Output: an NFA or None"""
  return incrementalInference(S_plus, S_minus, synthesizeByGA, accepted)
