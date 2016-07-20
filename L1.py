Sigma = ['a', 'b']

def dobre(s):
  if not re.match(r"\baa*bb*\b", s):
    return False
  ia, ib = 0, 0
  for c in s:
    if c == 'a':
      ia += 1
    else:
      ib += 1
  return ia <= ib