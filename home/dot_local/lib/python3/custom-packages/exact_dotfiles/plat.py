import errno
import os
import shutil

class plat:
  """Platform utilities."""

  # TODO Rename has_cmd
  @staticmethod
  def hascmd(*commands):
    """Check that all commands exist in PATH"""
    if not commands:
      raise ValueError("at least one command name must be given")
    for command in commands:
      if shutil.which(command) is None:
        return False
    return True

  # TODO Rename has_env
  @staticmethod
  def hasenv(*variables):
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
