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
  // t[f] == 1 iff |f| == 1; u[a, b, c] == 1 iff ab == c
  Parameters[Integers[0, 1], t[F], u[F, F, F],
    positives[F], negatives[F], dummy[K]],
  
  // w[i, f] == 1 iff from i we can derive factor f
  // y[i, j, l] == 1 iff there is a rule i -> j l
  // z[i, a] == 1 iff there is a rule i -> a
  Decisions[Integers[0, 1], w[K, F], y[K, K, K], z[K, F]], 
  
  // Minimize the number of grammar rules
  Goals[Minimize[FilteredSum[{i, K}, {a, F}, t[a] == 1, z[i, a]] + 
    Sum[{i, K}, {j, K}, {l, K}, 2*y[i, j, l]]]],

  Constraints[
    // Every example can be derived from the start symbol 0
    FilteredForeach[{s, F}, positives[s] == 1,  w[0, s] == 1],
    // None of the counterexamples can be derived from 0
    FilteredForeach[{s, F}, negatives[s] == 1,  w[0, s] == 0],
    // There is no rule of the form i -> a a ...
    FilteredForeach[{s, F}, {i, K}, t[s] == 0, z[i, s] == 0],
    // Relation between y, z, and w
    Foreach[{i, K}, {f, F},
      w[i, f] == 1 -: (FilteredSum[{b, F}, {c, F}, {j, K}, {l, K}, 
        u[b, c, f] == 1, y[i, j, l]*w[j, b]*w[l, c]] + z[i, f]) >= 1],
    Foreach[{i, K}, {f, F},
      w[i, f] == 0 -: (FilteredSum[{b, F}, {c, F}, {j, K}, {l, K},
        u[b, c, f] == 1, y[i, j, l]*w[j, b]*w[l, c]] + z[i, f]) == 0]
  ]
]"""

def varsToCFG(y, z):
  """Builds a CFG from variables
  Input: iterator over iterators
  Output: a CFG"""
  g = set()
  for i in y:
    if int(i[0]):
      g.add(tuple(map(int, i[1:])))
  for i in z:
    if int(i[0]):
      g.add((int(i[1]), i[2]))
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
            table.Rows.Add(a, b, c, 1 if a+b == c else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", \
      "A", "B", "C")
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
      if d.Name == "y":
        y = d.GetValues()
      if d.Name == "z":
        z = d.GetValues()
    cfg = varsToCFG(y, z)
    context.ClearModel()
    return cfg
  else:
    context.ClearModel()
    return None
