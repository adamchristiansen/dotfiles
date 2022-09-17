import select
import sys
import termios
import tty

class keymonitor:
  """Non-blocking keypress reader."""

  def __init__(self, nested=None):
    """
    Create a new listener. If nesting listeners then pass the parent as the
    argument to make sure that stdin is not reset while the parent needs it.
    """
    self._nested = nested
    self._settings = termios.tcgetattr(sys.stdin)

  def __enter__(self):
    if self._nested is None:
      tty.setcbreak(sys.stdin.fileno())
    return self

  def __exit__(self, _exc_type, _exc_value, _traceback):
    if self._nested is None:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._settings)

  def press(self):
    """Test if a key was pressed."""
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

  def get(self):
    """Get the pressed key."""
    return sys.stdin.read(1) if self.press() else None
