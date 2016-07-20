Sigma = ['a', 'b']

Lukasiewicz_parser = Parser({(0, 'b'), (0, ('a', 0, 0))})

def dobre(s):
  return Lukasiewicz_parser.accepts(s) > 0
