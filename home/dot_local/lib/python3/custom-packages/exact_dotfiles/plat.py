import abc
import errno
import os
import shutil

from .log import log

class MagicShell(abc.ABC):
  """Magically run a method when a specific shell is used."""

  def magic_bourne(self):
    """Use for Bourne-like shells."""
    pass
  def magic_csh(self):
    """Use for C-like shells."""
    pass
  def magic_elvish(self):
    """Use for Elvish shells."""
    pass
  def magic_shell(self, shell=None):
    """Magically determine the shell."""
    if shell is None:
      shell = os.path.basename(os.environ["SHELL"])
    if shell in ["ash", "bash", "dash", "sh", "zsh"]:
      return self.magic_bourne()
    elif shell in ["csh", "fish"]:
      return self.magic_csh()
    elif shell in ["elvish"]:
      return self.magic_elvish()
    else:
      log.fatal(f"unknown shell: {shell}")

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

  magic_shell = MagicShell
