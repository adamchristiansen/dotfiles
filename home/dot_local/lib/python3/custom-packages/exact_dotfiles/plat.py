import abc
import errno
import os
import shutil

from . import log
from .run import run

class magic_shell(abc.ABC):
  """Magically run a method when a specific shell is used."""

  def magic_posix(self):
    """Use for POSIX shells."""
    pass

  def magic_csh(self):
    """Use for C-like shells."""
    pass

  def magic_shell(self, shell=None):
    """Magically determine the shell."""
    if shell is None:
      # Look at the invocation of the parent process (which should be the
      # shell) to determine the shell type
      r = run(["ps", "-o", "comm", "-p", str(os.getppid())])
      if r.exitcode != 0:
        log.fatal("could not determine shell")
      abs_shell = r.stdout.splitlines()[1].strip().lstrip("-")
      shell = os.path.basename(abs_shell)
    if shell in ["ash", "bash", "dash", "sh", "zsh"]:
      return self.magic_posix()
    elif shell in ["csh", "fish"]:
      return self.magic_csh()
    else:
      log.fatal(f"unknown shell: {shell}")

def has_cmd(*commands):
  """Check that all commands exist in PATH"""
  if not commands:
    raise ValueError("at least one command name must be given")
  for command in commands:
    if shutil.which(command) is None:
      return False
  return True

def has_env(*variables):
  """Check that all environment variables are defined."""
  if not variables:
    raise ValueError("at least one variable name must be given")
  for variable in variables:
    if os.getenv(variable) is None:
      return False
  return True

def pid_exists(pid):
  """Check that pid exists."""
  if pid == 0:
    return True
  try:
    os.kill(pid, 0)
  except OSError as err:
    return err.errno == errno.EPERM
  return True
