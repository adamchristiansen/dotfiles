import collections
import os
import subprocess

RunResult = collections.namedtuple("Run", ["exitcode", "stdout", "stderr"])

def run(cmd, input=None, check=False, append_env=None, capture=True):
  """
  Run a command specified as a list of strings. The optional input is used for
  stdin. Environment variables can be added with append environment option. The
  capture option causes stdout and stderr to be captured in strings. An
  exception is raised on error when check is set. Returns the exitcode, stdout,
  and stderr of the command.
  """
  env = None
  if append_env is not None and append_env:
    env = {**os.environ, **append_env}
  p = subprocess.run(
    cmd,
    input=input,
    stdout=subprocess.PIPE if capture else None,
    stderr=subprocess.PIPE if capture else None,
    check=check,
    env=env)
  return RunResult(
    p.returncode,
    (p.stdout if p.stdout is not None else b"").decode("utf-8").strip(),
    (p.stderr if p.stderr is not None else b"").decode("utf-8").strip(),
  )
