import sys

class exit:
  """
  Exit a program.
  """

  @staticmethod
  def success():
    """Exit a program successfully."""
    sys.exit(0)

  @staticmethod
  def failure(exitcode=None):
    """Exit a program with a failure."""
    if exitcode is None or exitcode == 0:
      exitcode = 1
    sys.exit(exitcode)
