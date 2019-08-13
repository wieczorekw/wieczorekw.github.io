from z3 import *
from FAdo.fa import DFA
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
import time
import argparse

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

def encode(Sp, Sm, alphabet, NSTATES):
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

  for positive in Sp:
    s.add(g(x[positive]))
  for negative in Sm:
    s.add(Not(g(x[negative])))

  s.add(x[''] == 0)

  for node in PreOrderIter(nodes['']):
    if not node.is_root:
      w1, w2 = node.parent.name, node.name
      s.add(f[w2[-1]](x[w1], x[w2]))
      for i in range(NSTATES + 1):
        s.add(Implies(f[w2[-1]](x[w1], i), x[w2] == i))

  return s, f, g

def decode(model, f, g, alphabet, NSTATES):
  A = DFA()
  for i in range(NSTATES + 1):
    A.addState()
  A.setInitial(0)
  for i in range(NSTATES + 1):
    if model.eval(g(i)):
      A.addFinal(i)
  for a in alphabet:
    for q1 in range(NSTATES + 1):
      for q2 in range(NSTATES + 1):
        if model.eval(f[a](q1, q2)):
          A.addTransition(q1, a, q2)
  return A

def synthesize(S_plus, S_minus, alphabet, k):
  s, f, g = encode(S_plus, S_minus, alphabet, k)
  if sat == s.check():
    m = s.model()
    # print(m)
    return decode(m, f, g, alphabet, k)
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
  print(a.Final)
  print(a.delta)

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='an input file in Abbadingo format', type=str, default="train.txt")
parser.add_argument('--output', help='an output file in yaml format', type=str, default="result.yaml")
args = parser.parse_args()
X, Y = readWords(args.file)

if X & Y:
  print("Wspolne slowa:", X & Y)
  sys.exit()
print(X)
print(len(X))
print(Y)
print(len(Y))

NSTATES = 1
alphabet = set(a for w in X | Y for a in w)
while True:
  print("{}-{}".format(0, NSTATES))
  start_time = time.time()
  a = synthesize(X, Y, alphabet, NSTATES)
  working_time = time.time() - start_time
  print("Czas = %.2f s" % working_time)
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
