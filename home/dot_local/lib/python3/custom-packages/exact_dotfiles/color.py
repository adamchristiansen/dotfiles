# ANSI color escapes
COLOR = {
  None:      "\033[0m",
  "normal":  "\033[0m",
  "bold":    "\033[1m",
  "black":   "\033[30m",
  "red":     "\033[31m",
  "green":   "\033[32m",
  "yellow":  "\033[33m",
  "blue":    "\033[34m",
  "magenta": "\033[35m",
  "cyan":    "\033[36m",
  "white":   "\033[37m",
}

def spec(color, bold):
  """Produce a color spec."""
  return [color] + (["bold"] if bold else [])

class Color:
  """Provide coloring capability."""

  def __init__(self):
    pass

  def __call__(self, s, *colors):
    """
    Color text according to the colors provided. The last color has the greatest
    priority.
    """
    return "".join(map(lambda c: COLOR[c.lower()], colors)) + s + COLOR[None]

  def normal(self, s, bold=False):
    """Produce normal colored text."""
    return self(s, "normal")

  def bold(self, s, bold=False):
    """Produce bold text."""
    return self(s, "bold")

  def black(self, s, bold=False):
    """Produce black text."""
    return self(s, *spec("black", bold))

  def red(self, s, bold=False):
    """Produce red text."""
    return self(s, *spec("red", bold))

  def green(self, s, bold=False):
    """Produce green text."""
    return self(s, *spec("green", bold))

  def yellow(self, s, bold=False):
    """Produce yello text."""
    return self(s, *spec("yellow", bold))

  def blue(self, s, bold=False):
    """Produce blue text."""
    return self(s, *spec("blue", bold))

  def magenta(self, s, bold=False):
    """Produce magenta text."""
    return self(s, *spec("magenta", bold))

  def cyan(self, s, bold=False):
    """Produce cyan text."""
    return self(s, *spec("cyan", bold))

  def white(self, s, bold=False):
    """Produce white text."""
    return self(s, *spec("white", bold))

# This is the public color object
color = Color()
