import collections
import subprocess

"""
The output of a command.

- `exitcode` (int)
- `stdout` (str)
- `stderr` (str)
"""
Run = collections.namedtuple("Run", ["exitcode", "stdout", "stderr"])

def run(cmd):
    """
    Run a command.

    # Arguments

    - cmd (list<str>): The command to run.

    # Returns

    (Run): The command output.
    """
    ENCODING = "utf-8"
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return Run(
        p.returncode,
        stdout = (p.stdout if p.stdout is not None else b"").decode(ENCODING).strip(),
        stderr = (p.stderr if p.stderr is not None else b"").decode(ENCODING).strip(),
    )
