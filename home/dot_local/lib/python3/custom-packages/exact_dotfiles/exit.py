import sys

def success():
  """Exit a program successfully."""
  sys.exit(0)

def failure(exitcode=None):
  """Exit a program with a failure."""
  if exitcode is None or exitcode == 0:
    exitcode = 1
  sys.exit(exitcode)
