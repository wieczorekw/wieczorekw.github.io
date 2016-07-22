class Parser(object):
  """A parser class for QGNF grammars"""
  
  def __init__(self, productions):
    self.__prods = set()
    for p in productions:
      if isinstance(p[1], tuple):
        self.__prods.add((p[0],) + p[1])
      else:
        self.__prods.add(p)
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
    Output: an int"""
    self.__cache.clear()
    return self.__parse(word, 0)
  
  def grammar(self):
    return self.__prods
