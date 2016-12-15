from FAdo.fa import *
from FAdo.reex import *
import sys
sys.path.append(r"..\Ch3")
from Ktails import synthesize

def moves(w):
  result = set()
  n = len(w)
  if w[:3] == '110':
    result.add('1' + w[3:])
  for i in xrange(2, n-2):
    if w[i-2:i+1] == '011':
      result.add(w[:i-2] + '100' + w[i+1:])
    if w[i:i+3] == '110':
      result.add(w[:i] + '001' + w[i+3:])
  if w[-3:] == '011':
    result.add(w[:-3] + '1')
  return result

def pegnum(w):
  c = 0
  for i in xrange(len(w)):
    if w[i] == '1':
      c += 1
  return c

def generateExamples(n):
  """Generates all peg words of length <= n
  Input: n in {12, 15}
  Output: the set of examples"""
  rexp = str2regexp("1(1 + 01 + 001)*")
  raut = rexp.toNFA()
  g = EnumNFA(raut)
  numWords = {12: 1104, 15: 6872}[n]
  g.enum(numWords)
  words = sorted(g.Words, \
    cmp = lambda x, y: cmp(pegnum(x), pegnum(y)))
  S_plus = {'1', '11'}
  for i in xrange(4, numWords):
    if moves(words[i]) & S_plus:
      S_plus.add(words[i])
  return S_plus

def allWords(n):
  """Generates all words over {0, 1} up to length n
  Input: an integer n
  Output: all w in (0 + 1)* such that 1 <= |w| <= n"""
  rexp = str2regexp("(0 + 1)(0 + 1)*")
  raut = rexp.toNFA()
  g = EnumNFA(raut)
  g.enum(2**(n+1) - 2)
  return set(g.Words)
  
Train_pos = generateExamples(12)
Test_pos = generateExamples(15)
Test_neg = allWords(15) - Test_pos

for A in synthesize(Train_pos):
  if all(A.evalWordP(w) for w in Test_pos) \
    and not any(A.evalWordP(w) for w in Test_neg):
    Amin = A.toDFA().minimalHopcroft()
    print Amin.Initial, Amin.Final, Amin.delta
    break
