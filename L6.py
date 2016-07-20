Sigma = ['a', 'b']

def dobre(s):
  ia, ib = 0, 0
  for c in s:
    if c == 'a':
      ia += 1
    else:
      ib += 1
  return 2*ia == ib and len(s) > 0