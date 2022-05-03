# This can be run as python2 or python3

import argparse
import json

def indent(text, n=2):
  """
  Indent some text with the specified number of spaces.
  """
  return "\n".join(map(lambda line: 2 * " " + line, text.split("\n")))

def comp_hex(x):
  """
  Get the components of a hex RGB color as strings (`"00"` to `"ff"`).
  """
  return x[0:2], x[2:4], x[4:6]

def comp_rgb(x):
  """
  Get the components of a hex RGB color as integers (`0` to `255`).
  """
  return int(x[0:2], 16), int(x[2:4], 16), int(x[4:6], 16)

def comp_dec(x):
  """
  Get the components of a hex RGB color as floats (`0.0` to `1.0`).
  """
  f = lambda x: float(x) / 255
  r, g, b = comp_rgb(x)
  return f(r), f(g), f(b)

class Scheme:
  """
  Generate a chezmoi color scheme.
  """

  def __init__(self, filename):
    """
    Load color information from a file.
    """
    # Load the data from a file
    with open(filename) as f:
      data = json.load(f)
    # Fill the instance data
    self._theme = data["theme"]
    self._base = list(map(lambda base: data[base],
      sorted(filter(lambda c: c.startswith("base"), data.keys()))))
    self._wall = data["wall"]

  def _json_one(self, x):
    """
    Generate the JSON for one color, where `x` is the hx RGB string of the
    color.
    """
    d = {}
    d["hex"] = {}
    d["hex"]["rgb"] = x
    d["hex"]["bgr"] = comp_hex(x)[2] + comp_hex(x)[1] + comp_hex(x)[0]
    d["hex"]["r"] = comp_hex(x)[0]
    d["hex"]["g"] = comp_hex(x)[1]
    d["hex"]["b"] = comp_hex(x)[2]
    d["rgb"] = {}
    d["rgb"]["r"] = comp_rgb(x)[0]
    d["rgb"]["g"] = comp_rgb(x)[1]
    d["rgb"]["b"] = comp_rgb(x)[2]
    d["dec"] = {}
    d["dec"]["r"] = "{:.09f}".format(comp_dec(x)[0])
    d["dec"]["g"] = "{:.09f}".format(comp_dec(x)[1])
    d["dec"]["b"] = "{:.09f}".format(comp_dec(x)[2])
    return d

  def json(self):
    """
    Generate the JSON for the entire scheme.
    """
    d = {}
    d["theme"] = self._theme
    for i in range(16):
      d["base{:02x}".format(i)] = self._json_one(self._base[i])
    d["wall"] = self._json_one(self._wall)
    return json.dumps(d, indent=2, sort_keys=True)

if __name__ == "__main__":
  import os

  parser = argparse.ArgumentParser(description="Generate color schemes")
  parser.add_argument("colorscheme", metavar="S", type=str,
    help="The name of the colorscheme to generate")
  args = parser.parse_args()

  # Get the path to a colorscheme relative to this file
  filename = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    args.colorscheme + ".json")

  print(Scheme(filename).json())
