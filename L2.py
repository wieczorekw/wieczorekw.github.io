Sigma = ['a', 'b']

def dobre(s):
  l = 0
  for c in s:
    if l < 0:
      return False
    l += 1 if c == 'a' else -1
  return l == 0 and len(s) > 0
