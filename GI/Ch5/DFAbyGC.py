import clr
clr.AddReference('Microsoft.Solver.Foundation')
clr.AddReference('System.Data')
clr.AddReference('System.Data.DataSetExtensions')
from Microsoft.SolverFoundation.Services import *
from System.Data import DataTable, DataRow
from System.Data.DataTableExtensions import *
from System.IO import *
from FAdo.fa import *
import sys
sys.path.append(r"..\Ch2")
from Preliminaries2 import buildPTA

strModel = """Model[
  Parameters[Sets, A, Q],
  Parameters[Integers[0, 1], delta[Q, A, Q], F[Q], R[Q]],
  Decisions[Integers[1, %d], x[Q]],
  Constraints[
    FilteredForeach[{p, Q}, {q, Q}, 
      F[p] == 1 & R[q] == 1, Unequal[x[p], x[q]]
    ],
    FilteredForeach[{a, A}, {i, Q}, {j, Q}, {k, Q}, {l, Q},
      delta[i, a, j] == 1 & delta[k, a, l] == 1, 
        (x[i] == x[k]) -: (x[j] == x[l])
    ]
  ],
  Goals[Minimize[Max[Foreach[{q, Q}, x[q]]]]]
]"""

def inducedDFA(P, A):
  """Join groups of states for a new automaton
  Input: the partition P (the list of frozensets) and an DFA A
  Output: a new DFA, A/P"""
  B = DFA()
  d = dict()
  K = range(len(A.States))
  for p in P:
    d[p] = j = B.addState(p)
    if A.Initial in p:
      B.setInitial(j)
    if p & A.Final:
      B.addFinal(j)
    for state in p:
      K[state] = j
  for q in A.delta:
    for a in A.delta[q]:
      r = A.delta[q][a]
      B.addTransition(K[q], a, K[r])
  return B

def buildAPTA(Sp, Sm):
  """Builds an augmented PTA
  Input: a sample
  Output: a DFA"""
  aut = buildPTA(Sp | Sm)
  i = -1
  for w in aut.States:
    i += 1
    if w in Sm:
      aut.delFinal(i)  
  return aut
  
def xsToDFA(v, aut):
  """Builds a DFA from variables
  Input: iterator over values (x[0] = value, x[1] = index)
  Output: a DFA"""
  t = dict()
  for x in v:
    if int(x[0]) in t:
      t[int(x[0])].add(int(x[1]))
    else:
      t[int(x[0])] = {int(x[1])}
  partition = map(frozenset, t.itervalues())
  return inducedDFA(partition, aut)
  
def synthesize(S_plus, S_minus):
  """Finds a minimal DFA consistent with the input
  Input: a sample, S = (S_plus, S_minus)
  Output: a DFA"""
  apta = buildAPTA(S_plus, S_minus)  
  context = SolverContext.GetContext()
  context.LoadModel(FileFormat.OML, StringReader(strModel % len(apta)))
  parameters = context.CurrentModel.Parameters
  for i in parameters:
    if i.Name == "delta":
      table = DataTable()
      table.Columns.Add("Q1", int)
      table.Columns.Add("A", str)
      table.Columns.Add("Q2", int)
      table.Columns.Add("Value", int)
      for q1 in xrange(len(apta)):
        for a in apta.Sigma:
          for q2 in xrange(len(apta)):
            if q1 in apta.delta and a in apta.delta[q1] \
              and q2 == apta.delta[q1][a]:
              table.Rows.Add(q1, a, q2, 1)
            else:
              table.Rows.Add(q1, a, q2, 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "Q1", "A", "Q2")
    if i.Name == "F":
      table = DataTable()
      table.Columns.Add("Q", int)
      table.Columns.Add("Value", int)
      for q in xrange(len(apta)):
        table.Rows.Add(q, 1 if q in apta.Final else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "Q")
    if i.Name == "R":
      table = DataTable()
      table.Columns.Add("Q", int)
      table.Columns.Add("Value", int)
      q = -1
      for w in apta.States:
        q += 1
        table.Rows.Add(q, 1 if w in S_minus else 0)
      i.SetBinding[DataRow](AsEnumerable(table), "Value", "Q")
  solution = context.Solve()
  for d in solution.Decisions:
    if d.Name == "x":
      aut = xsToDFA(d.GetValues(), apta)
  context.ClearModel()
  return aut
