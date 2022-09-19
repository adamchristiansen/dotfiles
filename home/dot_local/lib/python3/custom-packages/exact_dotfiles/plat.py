import errno
import os
import shutil

class plat:
  """Platform utilities."""

  @staticmethod
  def has_cmd(*commands):
    """Check that all commands exist in PATH"""
    if not commands:
      raise ValueError("at least one command name must be given")
    for command in commands:
      if shutil.which(command) is None:
        return False
    return True

  @staticmethod
  def has_env(*variables):
    """Check that all environment variables are defined."""
    if not variables:
      raise ValueError("at least one variable name must be given")
    for variable in variables:
      if os.getenv(variable) is None:
        return False
    return True

  @staticmethod
  def pid_exists(pid):
    """Check that pid exists."""
    if pid == 0:
      return True
    try:
      os.kill(pid, 0)
    except OSError as err:
      return err.errno == errno.EPERM
    return True
