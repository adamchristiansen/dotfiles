# ANSI color escapes
_COLOR = {
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

def _spec(color, bold):
  """Produce a color specification."""
  return [color] + (["bold"] if bold else [])

def color(s, *colors):
  """Color text. The last color has the greatest priority."""
  return "".join(map(lambda c: _COLOR[c.lower()], colors)) + s + _COLOR[None]

def normal(s, bold=False):
  """Produce normal colored text."""
  return color(s, "normal")

def bold(s, bold=False):
  """Produce bold text."""
  return color(s, "bold")

def black(s, bold=False):
  """Produce black text."""
  return color(s, *_spec("black", bold))

def red(s, bold=False):
  """Produce red text."""
  return color(s, *_spec("red", bold))

def green(s, bold=False):
  """Produce green text."""
  return color(s, *_spec("green", bold))

def yellow(s, bold=False):
  """Produce yello text."""
  return color(s, *_spec("yellow", bold))

def blue(s, bold=False):
  """Produce blue text."""
  return color(s, *_spec("blue", bold))

def magenta(s, bold=False):
  """Produce magenta text."""
  return color(s, *_spec("magenta", bold))

def cyan(s, bold=False):
  """Produce cyan text."""
  return color(s, *_spec("cyan", bold))

def white(s, bold=False):
  """Produce white text."""
  return color(s, *_spec("white", bold))
