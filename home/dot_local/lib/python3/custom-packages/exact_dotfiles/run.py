import collections
import subprocess

RunResult = collections.namedtuple("Run", ["exitcode", "stdout", "stderr"])

def run(cmd, input=None, check=False):
  """
  Run a command specified as a list of strings. The optional input is used for
  stdin. An exception is raised on error when check is set. Returns the
  exitcode, stdout, and stderr of the command.
  """
  p = subprocess.run(
    cmd,
    input=input,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=check)
  return RunResult(
    p.returncode,
    (p.stdout if p.stdout is not None else b"").decode("utf-8").strip(),
    (p.stderr if p.stderr is not None else b"").decode("utf-8").strip(),
  )
