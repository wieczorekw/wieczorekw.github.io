import random
from copy import deepcopy

NUMBER_OF_ITERATIONS = 2000
NUMBER_OF_VARIABLES = 12
S_PLUS_SIZE = 100
TOURNAMENT_SIZE = 7

X = set()
Y = set()
uncovered = set()
Predicted_grammars = set()

def readXandY(filePath, X, Y):
  inList = open(filePath, 'rU').readlines()
  for line in inList:
    words = line.split()
    if words[0] == "1":
      X.add(words[2])
    if words[0] == "0":
      Y.add(words[2])

def odczytajTestowe(lines):
  slowa = []
  for line in lines:
    r = line.split()
    slowo = r[2]
    slowa.append(slowo)
  return slowa

class Parser(object):
  """A parser class for CNF grammars"""
  
  def __init__(self, productions):
    self.__prods = productions
    self.__cache = dict()
    
  def __parse(self, w, var):
    """Unger's parsing method
    Input: a word, a non-terminal (an integer)
    Output: true or false"""
    if (w, var) in self.__cache:
      return self.__cache[w, var]
    else:
      n = len(w)
      if n == 1: return (var, w) in self.__prods
      for p in self.__prods:
        if p[0] == var:
          if len(p) == 3:
            for i in range(1, n):
              if self.__parse(w[:i], p[1]) and self.__parse(w[i:], p[2]):
                self.__cache[w, var] = True
                return True
      self.__cache[w, var] = False
      return False
      
  def accepts(self, word):
    """Membership query
    Input: a string
    Output: true or false"""
    self.__cache.clear()
    return self.__parse(word, 0)
    
  def grammar(self):
    return self.__prods

def catenate(A, B):
  return set(a+b for a in A for b in B)
  
def grammar2words(G):
  """Works only for non-circular CFGs"""
  words = dict((r[0], set()) for r in G)
  for prod in G:
    if len(prod) == 2:
      words[prod[0]].add(prod[1])
  prods = set(r for r in G if len(r) == 3)
  vars = set()
  while prods:
    vars.update(r[0] for r in prods)
    for (v1, v2, v3) in prods:
      if not (v2 in vars or v3 in vars):
        words[v1].update(catenate(words[v2], words[v3]))
        prods.remove((v1, v2, v3))
        vars.clear()
        break
  return words[0]

def determineACC(grammar, S_plus, S_minus):
  parser = Parser(grammar)
  p = len(S_plus)
  n = len(S_minus)
  tp = 0
  for word in S_plus:
    tp += (1 if parser.accepts(word) else 0)
  tn = 0
  for word in S_minus:
    tn += (0 if parser.accepts(word) else 1)
  return (tp/p + tn/n)/2
  
class Node:
  def __init__(self, subword):
    self.number = 0
    d = len(subword)
    if d == 1:
      self.terminal = subword
      self.height = 0
    else:
      r = random.randint(1, d-1)
      self.left = Node(subword[:r])
      self.right = Node(subword[r:])
      self.height = 1 + max(self.left.height, self.right.height)
  def randomize_idxes(self, minidx=0, maxidx=0):
    self.number = random.randint(minidx, maxidx)
    if self.height > 0:
      self.left.randomize_idxes(self.number + 1, max(self.number + 1, NUMBER_OF_VARIABLES - self.left.height))
      self.right.randomize_idxes(self.number + 1, max(self.number + 1, NUMBER_OF_VARIABLES - self.right.height))
  def get_rules(self):
    if self.height == 0:
      return frozenset([(self.number, self.terminal)])
    else:
      return self.left.get_rules() | self.right.get_rules() | {(self.number, self.left.number, self.right.number)}
  def printIt(self, p=0):
    if self.height == 0:
      for i in range(p):
        print("     |", end="")
      print("{0:-<5}{1}".format(self.number, self.terminal))
    else:
      self.right.printIt(p+1)    
      for i in range(p):
        print("     |", end="")
      print("{0:-<5}|".format(self.number))
      self.left.printIt(p+1)
  def all_nodes(self, father=None, side=""):
    if self.height == 0:
      return ((self, father, side),)
    else:
      return ((self, father, side),) + self.left.all_nodes(self, "left") + self.right.all_nodes(self, "right")
  
class Individual:
  def __init__(self, word):
    self.tree = Node(word)
    self.tree.randomize_idxes()
    self.update()
  def update(self):
    self.grammar = self.tree.get_rules()
    self.fitness = determineACC(self.grammar, S_plus, S_minus)
  @staticmethod
  def crossover(i1, i2):
    c1 = deepcopy(i1)
    c2 = deepcopy(i2)
    n1 = c1.tree.all_nodes()
    n2 = c2.tree.all_nodes()
    for i in range(4):
      (son1, father1, side1) = random.choice(n1)
      (son2, father2, side2) = random.choice(n2)
      if son1.number <= son2.number:
        if father1:
          if side1 == 'left':
            father1.left = son2
          else:
            father1.right = son2
        else:
          c1.tree = son2
          c1.tree.number = 0
        break
    return c1
  def mutate(self):
    ns = self.tree.all_nodes()
    (son, father, side) = random.choice(ns)
    if father:
      if son.number > father.number + 1:
        son.number = random.randint(father.number + 1, son.number - 1)
  
random.seed()
readXandY("tren.txt", X, Y)
uncovered.update(X)
list_of_Y = list(Y)
testowe = odczytajTestowe(open("test.txt", "r").readlines())

step = 0
while uncovered:
  step += 1
  print(step)
  list_of_uncovered = list(uncovered)
  S_plus = [random.choice(list_of_uncovered) for j in range(S_PLUS_SIZE)]
  S_minus = [random.choice(list_of_Y) for j in range(S_PLUS_SIZE)]
  P = [Individual(w) for w in S_plus]
  for iteration in range(NUMBER_OF_ITERATIONS):
    *rest, parent1, parent2 = sorted(random.sample(P, TOURNAMENT_SIZE), key = lambda i: i.fitness)
    child1 = Individual.crossover(parent1, parent2) 
    child2 = Individual.crossover(parent2, parent1)
    child1.mutate()
    child2.mutate()
    child1.update()
    child2.update()    
    *rest, best1, best2 = sorted([parent1, parent2, child1, child2], key = lambda i: i.fitness)
    P[P.index(parent1)] = best1
    P[P.index(parent2)] = best2
  best = max(P, key = lambda i: i.fitness)
  parser = Parser(best.grammar)
  covered = set(w for w in uncovered if parser.accepts(w))
  if covered:
    uncovered -= covered
    Predicted_grammars.add(parser)
print("Predicted grammars: {}".format(len(Predicted_grammars)))

# Parsers = map(Parser, Predicted_grammars)
print(list(map(lambda s: int(any(p.accepts(s) for p in Predicted_grammars)), testowe)))
