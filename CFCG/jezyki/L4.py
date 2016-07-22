Sigma = ['a', 'b']

def dobre(s):
  d = len(s)
  if d < 2:
    return False
  if d % 2 == 0:
    lewe, prawe = s[:d/2], "".join(list(reversed(s[d/2:])))
  else:
    lewe, prawe = s[:d/2], "".join(list(reversed(s[d/2 + 1:])))
  return lewe == prawe
