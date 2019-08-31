from z3 import *
from networkx import *
from FAdo.fa import DFA
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
import time
import argparse

def maximum_independent_set(G):
    I = set()
    while G:
        v = min(G.nodes(), key = G.degree)
        I.add(v)
        G.remove_nodes_from(list(G.neighbors(v)))
        G.remove_node(v)
    return I

def prefixes(S):
  result = set()
  for s in S:
    for i in range(len(s) + 1):
      result.add(s[:i])
  return result

def catenate(A, B):
  return set(a+b for a in A for b in B)

def lq(w, X):
  U = set()
  l = len(w)
  for x in X:
    if x[:l] == w:
      U.add(x[l:])
  if w in X:
    U.add("")
  return U

def encode(Sp, Sm, alphabet, NSTATES, mis):
  S = Sp | Sm
  P = prefixes(S)
  # R = prefixes(Sm)
  nodes = dict( (w, Node(w)) for w in P )
  nodes[''].parent = None
  for w1 in P:
    for w2 in P:
      if w2 and w2[:-1] == w1:
        nodes[w2].parent = nodes[w1]

  s = Solver()
  x = dict( (p, Int("x_%s" % p)) for p in P )
  f = dict( (a, Function('f' + a, IntSort(), IntSort(), BoolSort())) for a in alphabet )
  g = Function('g', IntSort(), BoolSort())

  for p in P:
    s.add(x[p] >= 0)
    s.add(x[p] <= NSTATES)

  # s.add(x[''] == 0)
  ind = 0
  for p in mis:
    s.add(x[p] == ind)
    ind += 1

  for positive in Sp:
    s.add(g(x[positive]))
  for negative in Sm:
    s.add(Not(g(x[negative])))

  for node in PreOrderIter(nodes['']):
    if not node.is_root:
      w1, w2 = node.parent.name, node.name
      s.add(f[w2[-1]](x[w1], x[w2]))
      for i in range(NSTATES + 1):
        s.add(Implies(f[w2[-1]](x[w1], i), x[w2] == i))

  return s, x, g, P

def decode(model, x, g, P, alphabet, NSTATES):
  A = DFA()
  for i in range(NSTATES + 1):
    A.addState()
  A.setInitial(model.eval(x['']).as_long())
  for i in range(NSTATES + 1):
    if model.eval(g(i)):
      A.addFinal(i)
  for a in alphabet:
    for p in P:
      q1 = model.eval(x[p]).as_long()
      if p+a in P:
        q2 = model.eval(x[p+a]).as_long()
        if q1 not in A.delta or q2 not in A.delta[q1]:
          A.addTransition(q1, a, q2)
  return A

def synthesize(S_plus, S_minus, alphabet, k, mis):
  s, x, g, P = encode(S_plus, S_minus, alphabet, k, mis)
  if sat == s.check():
    m = s.model()
    # print(m)
    return decode(m, x, g, P, alphabet, k)
  else:
    return None

def rw(dmin, dmax, alphabet):
  d = random.randint(dmin, dmax)
  s = ""
  for i in range(d):
    s += random.choice(alphabet)
  return s

def readWords(file_name):
    """From Abbadingo competition format
    """
    positives = set()
    negatives = set()
    with open(file_name, encoding='utf-8') as file:
        it = iter(file)
        line = next(it)
        number_of_words = int(line.split()[0])
        for _ in range(number_of_words):
            line = next(it)
            cls, length, *symbols = line.split()
            s = "".join(symbols)
            if cls == '1':
                positives.add(s)
            else:
                negatives.add(s)
    assert len(positives & negatives) == 0
    return positives, negatives

def printAut(a):
    print("Automat:")
    print(a.Initial)
    print(a.Final)
    print(a.delta)

def buildPTA(S):
  """Build a prefix tree acceptor from examples
  Input: the set of strings, S
  Output: a DFA representing PTA"""
  A = DFA()
  q = dict()
  for u in prefixes(S):
    q[u] = A.addState(u)
  for w in iter(q):
    u, a = w[:-1], w[-1:]
    if a != '':
      A.addTransition(q[u], a, q[w])
    if w in S:
      A.addFinal(q[w])
  A.setInitial(q[''])
  return A

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

def canBeMerged(q1, q2, apta, Sp, Sm, alphabet):

    def check(q1, q2):
        if q1 == q2:
            return True
        if apta.States[q1] in Sp and apta.States[q2] in Sm or apta.States[q1] in Sm and apta.States[q2] in Sp:
            return False
        if q1 in apta.delta and q2 in apta.delta:
            for a in alphabet:
                if a in apta.delta[q1] and a in apta.delta[q2]:
                    r1 = apta.delta[q1][a]
                    r2 = apta.delta[q2][a]
                    if not check(r1, r2):
                        return False
        return True

    return check(q1, q2)

def maxIndependentSet(Sp, Sm, alphabet):
    print("Searching for maximum independent set ...")
    apta = buildAPTA(Sp, Sm)
    print("APTA build.")
    n = len(apta)
    G = Graph()
    G.add_nodes_from(range(n))
    for i in range(n - 1):
        for j in range(i + 1, n):
            if canBeMerged(i, j, apta, Sp, Sm, alphabet):
                G.add_edge(i, j)
    print("Graph prepared.")
    print("Search started.")
    ms = maximum_independent_set(G)
    print("Independent set of size", len(ms), "found.")
    return set(apta.States[j] for j in ms)

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='an input file in Abbadingo format', type=str, default="train.txt")
parser.add_argument('--output', help='an output file in yaml format', type=str, default="result.yaml")
args = parser.parse_args()
print('Working with file: {fileName}'.format_map({ 'fileName': args.file }))
X, Y = readWords(args.file)

if X & Y:
  print("Wspolne slowa:", X & Y)
  sys.exit()
# print(X)
# print(len(X))
# print(Y)
# print(len(Y))

whole_time = time.time()
alphabet = set(a for w in X | Y for a in w)
mis = maxIndependentSet(X, Y, alphabet)
NSTATES = len(mis) - 1
while True:
  print("{}-{}".format(0, NSTATES))
  a = synthesize(X, Y, alphabet, NSTATES, mis)
  if a:
    break
  NSTATES += 1
printAut(a)
print("Błędy dla pozytywnych:")
for x in X:
  if not a.evalWordP(x):
    print(x if x != '' else "epsilon", end = ' ')
print("\nBłędy dla negatywnych:")
for y in Y:
  if a.evalWordP(y):
    print(y if y != '' else "epsilon", end = ' ')
print('')
print("Pełny czas = %.2f s" % (time.time() - whole_time))
