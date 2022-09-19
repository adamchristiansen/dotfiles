import sys

from .color import color

LEVELS = {
  "debug": lambda s: color.magenta("DEBUG: ", bold=True) + color.magenta(s),
  "info": lambda s: color.blue("INFO: ", bold=True) + color.blue(s),
  "warn": lambda s: color.yellow("WARNING: ", bold=True) + color.yellow(s),
  "error": lambda s: color.red("ERROR: ", bold=True) + color.red(s),
  "fatal": lambda s: color.red("FATAL: ", bold=True) + color.red(s),
}

class log:
  """Log to the console in a pretty way."""

  @staticmethod
  def _log(message, stderr=False, level=None, exitcode=None):
    """
    A basic log print. Prints to stderr when stderr is true. The level can be
    "debug", "info", "warn", "error", or "fatal", which formats the message
    accordingly. When the level is "fatal", the program exits with exitcode if
    it is set, otherwise, the exitcode defaults to 1.
    """
    f = sys.stderr if stderr else sys.stdout
    fatal = False
    if level is not None:
      level = level.strip().lower()
      message = LEVELS[level](message)
      f = sys.stderr
      fatal = level == "fatal"
    print(message, file=f)
    if fatal:
      sys.exit(exitcode if exitcode is not None else 1)

  @staticmethod
  def debug(message):
    """Log with debug level."""
    log._log(message, level="debug")

  @staticmethod
  def info(message):
    """Log with info level."""
    log._log(message, level="info")

  @staticmethod
  def warn(message):
    """Log with warning level."""
    log._log(message, level="warn")

  @staticmethod
  def error(message):
    """Log with error level."""
    log._log(message, level="error")

  @staticmethod
  def fatal(message, exitcode=None):
    """Log with error level. Optionally set the exitcode"""
    log._log(message, level="fatal", exitcode=exitcode)
