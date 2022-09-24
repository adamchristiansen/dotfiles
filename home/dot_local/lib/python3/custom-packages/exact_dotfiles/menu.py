from . import exit as ex
from .run import run

def menu(options, index=False, exit=True, fail=True):
  """
  Show a menu with the provided options.

  When index is true, the index of the selected item is returned, and when
  false, the item itself is returned.

  When exit is true, the program exits when no item is selected. When fail is
  true, the program exits with a failure.
  """
  cmd = ["rofi", "-dmenu", "-i"]
  if index:
    cmd.extend(["-format", "i"])
  r = run(cmd)
  # Rofi returns non-zero when no selection is made
  if r.returncode != 0:
    if exit:
      log.fatal("menu error") if fail else ex.success()
    return None
  return int(r.stdout) if index else r.stdout
