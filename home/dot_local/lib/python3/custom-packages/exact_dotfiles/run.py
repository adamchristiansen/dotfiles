import collections
import subprocess

"""
The output of a command.

- `exitcode` (int)
- `stdout` (str)
- `stderr` (str)
"""
Run = collections.namedtuple("Run", ["exitcode", "stdout", "stderr"])

def run(cmd, input=None, check=False):
  """
  Run a command.

  # Arguments

  - cmd (list<str>): The command to run.
  - input (bytes|None): Optional input to stdin.
  - check (bool): Raise an exception on non-zero exitcode.

  # Returns

  (Run): The command output.
  """
  p = subprocess.run(
    cmd,
    input=input,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=check)
  return Run(
    p.returncode,
    (p.stdout if p.stdout is not None else b"").decode("utf-8").strip(),
    (p.stderr if p.stderr is not None else b"").decode("utf-8").strip(),
  )
