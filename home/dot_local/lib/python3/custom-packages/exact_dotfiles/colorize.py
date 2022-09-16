import sys

# ANSI color escapes
ESCAPES = {
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

def colorize(s, *colors):
  """
  Colorize a string based on color names. The available color names are:

  - normal
  - bold
  - black
  - red
  - green
  - yellow
  - blue
  - magenta
  - cyan
  - white

  If more than one color is supplied, the last color has the highest priority.
  """
  return "".join(map(lambda c: ESCAPES[c.lower()], colors)) + s + ESCAPES[None]
