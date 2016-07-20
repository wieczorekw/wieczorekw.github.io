Sigma = ['a', 'b']

def dobre(s):
  if re.match(r"\baa*bb*\b", s):
    return True
  else:
    return False
