import clr
clr.AddReference('Microsoft.Solver.Foundation')
clr.AddReference('System.Data')
clr.AddReference('System.Data.DataSetExtensions')
from Microsoft.SolverFoundation.Services import *
from System.Data import DataTable, DataRow
from System.Data.DataTableExtensions import *
from System.IO import *
from pipetools import pipe
import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import *

# OML Model string
strModel = """Model[
  // F = Factors built from S_+ (positives) and S_- (negatives)
  // {0, 1, ..., k-1} = K = grammar variables
  Parameters[Sets, F, K],
  // t[f] == 1 iff |f| == 1; u[a, b, c] == 1 iff ab == c; 
  // v[a, b, c, d] == 1 iff abc == d
  Parameters[Integers[0, 1], t[F], u[F, F, F], v[F, F, F, F], 
    positives[F], negatives[F], dummy[K]],
  
  // w[i, f] == 1 iff from i we can derived factor f
  // x[i, a, j, k] == 1 iff there is a rule i -> a j k
  // y[i, a, j] == 1 iff there is a rule i -> a j
  // z[i, a] == 1 iff there is a rule i -> a
  Decisions[Integers[0, 1], w[K, F], x[K, F, K, K], y[K, F, K], 
    z[K, F]], 
  
  // Minimize the number of grammar rules
  Goals[Minimize[FilteredSum[{i, K}, {a, F}, t[a] == 1, z[i, a]] + 
    FilteredSum[{i, K}, {a, F}, {j, K}, t[a] == 1, 2*y[i, a, j]] + 
      FilteredSum[{i, K}, {a, F}, {j, K}, {k, K}, t[a] == 1, 
        3*x[i, a, j, k]]]],

  Constraints[
    // Every example can be derived from the start symbol 0
    FilteredForeach[{s, F}, positives[s] == 1,  w[0, s] == 1],
    // None of the counterexamples can be derived from 1
    FilteredForeach[{s, F}, negatives[s] == 1,  w[0, s] == 0],
    // There is no rule of the form i -> a a ...
    FilteredForeach[{s, F}, {i, K}, t[s] == 0, z[i, s] == 0],
    // Relation between x, y, z, and w
    Foreach[{k, K}, {f, F},
      w[k, f] == FilteredSum[{a, F}, {b, F}, {c, F}, {i, K}, {j, K}, 
        v[a, b, c, f] == 1, x[k, a, i, j]*w[i, b]*w[j, c]] +
          FilteredSum[{a, F}, {b, F}, {i, K}, u[a, b, f] == 1, 
            y[k, a, i]*w[i, b]] + z[k, f]]
  ]
]"""
  
def varsToCFG(*v):
  """Builds a CFG from variables
  Input: iterator over iterators
  Output: a CFG"""
  g = set()
  for it in v:
    for i in it:
      if int(i[0]):
        g.add((int(i[1]), i[2]) + tuple(map(int, i[3:])))
  return g
    
def synthesize(S_plus, S_minus, k):
  """Finds a CFG with k non-terminals consistent with the input
  Input: a sample, S = (S_plus, S_minus), an integer k
  Output: a CFG (productions as the set of tuples) or None"""
  factors = pipe | prefixes | suffixes
  F = factors(S_plus | S_minus)
  F.remove("")
  context = SolverContext.GetContext()
  context.LoadModel(FileFormat.OML, StringReader(strModel))
  parameters = context.CurrentModel.Parameters
  for i in parameters:
    if i.Name == "t":
      table = DataTable()
      table.Columns.Add("F", str)
      table.Columns.Add("Value", int)
      for f in F:
        table.Rows.Add(f, 1 if len(f) == 1 else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "F")
    if i.Name == "u":
      table = DataTable()
      table.Columns.Add("A", str)
      table.Columns.Add("B", str)
      table.Columns.Add("C", str)
      table.Columns.Add("Value", int)
      for a in F:
        for b in F:
          for c in F:
            table.Rows.Add(a, b, c, 1 if len(a) == 1 and a+b == c else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "A", "B", "C")
    if i.Name == "v":
      table = DataTable()
      table.Columns.Add("A", str)
      table.Columns.Add("B", str)
      table.Columns.Add("C", str)
      table.Columns.Add("D", str)
      table.Columns.Add("Value", int)
      for a in F:
        for b in F:
          for c in F:
            for d in F:
              table.Rows.Add(a, b, c, d, 1 if len(a) == 1 and a+b+c == d else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "A", "B", "C", "D")
    if i.Name == "positives":
      table = DataTable()
      table.Columns.Add("F", str)
      table.Columns.Add("Value", int)
      for f in F:
        table.Rows.Add(f, 1 if f in S_plus else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "F")
    if i.Name == "negatives":
      table = DataTable()
      table.Columns.Add("F", str)
      table.Columns.Add("Value", int)
      for f in F:
        table.Rows.Add(f, 1 if f in S_minus else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "F")
    if i.Name == "dummy":
      table = DataTable()
      table.Columns.Add("K", int)
      table.Columns.Add("Value", int)
      for j in xrange(k):
        table.Rows.Add(j, 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "K")
  solution = context.Solve()
  if solution.Quality == SolverQuality.Optimal \
    or solution.Quality == SolverQuality.LocalOptimal:
    for d in solution.Decisions:
      if d.Name == "x":
        x = d.GetValues()
      if d.Name == "y":
        y = d.GetValues()
      if d.Name == "z":
        z = d.GetValues()
    cfg = varsToCFG(x, y, z)
    context.ClearModel()
    return cfg
  else:
    context.ClearModel()
    return None

class Parser(object):
  """A parser class for QGNF grammars"""
  
  def __init__(self, productions):
    self.__prods = productions
    self.__cache = dict()
    
  def __parse(self, w, var):
    """A parsing with checking that it is not ambiguous
    Input: a word, a non-terminal (an integer)
    Output: the number of ways of parsing"""
    if (w, var) in self.__cache:
      return self.__cache[w, var]
    else:
      n = len(w)
      if n == 1: return int((var, w) in self.__prods)
      counter = 0
      for p in self.__prods:
        if p[0] == var and p[1] == w[0]:
          if n > 2 and len(p) == 4:
            for i in xrange(2, n):
              cl = self.__parse(w[1:i], p[2])
              cr = self.__parse(w[i:], p[3])
              counter += cl*cr
          elif len(p) == 3:
            counter += self.__parse(w[1:], p[2])
      self.__cache[w, var] = counter
      return counter
      
  def accepts(self, word):
    """Membership query
    Input: a string
    Output: true or false"""
    self.__cache.clear()
    return self.__parse(word, 0) > 0
  
  def ambiguousParse(self, word):
    """Check if parsing is unambiguous
    Input: a string that is accepted by this parser
    Output: true or false"""
    self.__cache.clear()
    return self.__parse(word, 0) != 1
  
  def grammar(self):
    return self.__prods

NPOS = 12  # may be arbitrarily changed

def allWords(alphabet, n):
  """Returns Sigma^(<= n)
  Input: the set of chars and an integer
  Output: The set of strings"""
  lang = [set() for i in xrange(n+1)]
  lang[0].add('')
  for i in xrange(1, n+1):
    for w in lang[i-1]:
      for a in alphabet:
        lang[i].add(a+w)
  return reduce(set.__or__, lang)

def findGrammar(alphabet, belong_fun):
  """Main function
  Input: alphabet and a function that tells whether
  a given word belongs to a sought language
  Output: a grammar in QGNF (the set of tuples)"""
  all_words = allWords(alphabet, NPOS)
  all_words.remove('')
  X = [w for w in all_words if belong_fun(w)]
  Y = list(all_words - set(X))
  X.sort(key=len)
  Y.sort(key=len)
  k = 1
  Spos, Sneg = {X[0]}, {Y[0]}
  while True:
    print Spos
    print Sneg
    print k
    G = synthesize(Spos, Sneg, k)
    print G, '\n'
    while G == None:
      k += 1
      print Spos
      print Sneg
      print k
      G = synthesize(Spos, Sneg, k)
      print G, '\n'
    wp, wn = None, None
    p = Parser(G)
    for w in X:
      if not p.accepts(w):
        wp = w
        break
    for w in Y:
      if p.accepts(w):
        wn = w
        break
    if wp == None and wn == None:
      more_search = False
      for w in X:
        if p.ambiguousParse(w):
          Spos.add(w)
          more_search = True
          break
      if not more_search:
        break
    elif wp == None:
      Sneg.add(wn)
    elif wn == None:
      Spos.add(wp)
    else:
      if len(wp) <= len(wn):
        Spos.add(wp)
      else:
        Sneg.add(wn)
