import subprocess

# The menu command to run.
MENU_COMMAND = ["rofi", "-dmenu", "-i", "-format", "i"]

# The encoding for subprocess communication.
ENCODING = "utf-8"

def menu(options):
  """
  Run the menu command with the options provided.

  # Arguments

  - `options` (list<str>): The list of options to show.

  # Returns

  (int|None): An integer index into the `options` when an option was
  successfully selected. `None` is returned when the menu was cancelled or an
  error occurred.
  """
  r = subprocess.run(MENU_COMMAND,
    input="\n".join(options).encode(ENCODING),
    stdout=subprocess.PIPE)
  try:
    if r.returncode == 0:
      return int(r.stdout.decode(ENCODING).strip())
    else:
      return None
  except ValueError:
    return None
