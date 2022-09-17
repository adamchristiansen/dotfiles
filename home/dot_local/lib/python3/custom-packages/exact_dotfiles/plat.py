import os
import shutil

class plat:
  """Platform utilities."""

  @staticmethod
  def hascmd(*commands):
    """Check that all commands exist in PATH"""
    if not commands:
      raise ValueError("at least one command must be given")
    for command in commands:
      if shutil.which(command) is None:
        return False
    return True

  @staticmethod
  def hasenv(variables):
    """Check that all environment variables are defined."""
    if not commands:
      raise ValueError("at least one command must be given")
    for variable in variables:
      if os.getenv(variable) is None:
        return False
    return True
