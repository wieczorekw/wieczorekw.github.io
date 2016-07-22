import random

def J(G, S):
  result = []
  for j in G.nodes_iter():
    if (j not in S) and all(j in G[s] for s in S):
      result.append(j)
  return result

def choose_j(G, J_S):
  suma = sum(G.degree(j) + G.node[j]['tau'] for j in J_S)
  r = random.randint(1, suma)
  cum = 0
  for j in J_S:
    cum += G.degree(j) + G.node[j]['tau']
    if cum >= r:
      return j


def mClique(G):
  t = 0
  n = G.number_of_nodes()
  V = G.nodes()
  for v in V:
    G.node[v]['tau'] = 0
  tau = dict.fromkeys(V, 0)
  M, C, S = set(), set(), set()
  while True:
    t += 1
    C.clear()
    C |= M
    M.clear()
    for k in xrange(1, n+1):
      S.clear()
      i = random.choice(V)
      S.add(i)
      tab = J(G, S)
      while len(tab) > 0:
        j = choose_j(G, tab)
        S.add(j)
        tab = J(G, S)
      size = len(S)
      for j in S:
        tau[j] += size
    if size > len(M):
      M.clear()
      M |= S
    for v in V:
      G.node[v]['tau'] += tau[v]
      tau[v] = 0
    if len(C) >= len(M):
      return C
