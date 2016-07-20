Sigma = ['a', 'b', 'c']
MAXLEN = 10
DLEN = 8

def dobre(s):
  if not re.match(r"\baa*bb*cc*\b", s):
    return False
  i, j, k = 0, 0, 0
  for c in s:
    if c == 'a':
      i += 1
    elif c == 'b':
      j += 1
    else:
      k += 1
  return i == j or j == k
  