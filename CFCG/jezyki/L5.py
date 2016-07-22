Sigma = ['a', 'b']

def dobre(s):
  ia, ib = 0, 0
  for c in s:
    if c == 'a':
      ia += 1
    else:
      ib += 1
  return ia == ib and len(s) > 0