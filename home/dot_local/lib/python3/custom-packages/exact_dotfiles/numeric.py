def clamp(v, lo, hi):
  """
  Clamp a value between low and high limits.
  """
  return lo if v < lo else (hi if v > hi else v)
