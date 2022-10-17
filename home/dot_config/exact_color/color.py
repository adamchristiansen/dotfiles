#!/usr/bin/env python3

import argparse
import json
import os

# Maps a name to base color for names colors.
NAME_TO_BASE = {
  'bg':     0x00,
  'black':  0x03,
  'fg':     0x05,
  'white':  0x05,
  'red':    0x08,
  'orange': 0x09,
  'yellow': 0x0a,
  'green':  0x0b,
  'cyan':   0x0c,
  'blue':   0x0d,
  'pink':   0x0e,
  'purple': 0x0f,
}

def indent(text, n=2):
  """Indent some text with the specified number of spaces."""
  return '\n'.join(map(lambda line: 2 * ' ' + line, text.split('\n')))

def comp_hex(x):
  """Get the components of a hex RGB color as strings (00 to ff)."""
  return x[0:2], x[2:4], x[4:6]

def comp_rgb(x):
  """Get the components of a hex RGB color as integers (0 to 255)."""
  return int(x[0:2], 16), int(x[2:4], 16), int(x[4:6], 16)

def comp_dec(x):
  """Get the components of a hex RGB color as floats (0.0 to 1.0)."""
  return list(map(lambda x: float(x) / 255, comp_rgb(x)))

class Scheme:
  """Generate a chezmoi color scheme."""

  def __init__(self, filename, special):
    """Load color information from a file."""
    # Load the data from a file
    with open(filename) as f:
      data = json.load(f)
    # Fill the instance data
    self._theme = data['theme']
    self._base = list(map(lambda base: data[base],
      sorted(filter(lambda c: c.startswith('base'), data.keys()))))
    self._wall = data['wall']
    self._special = special

  def _json_one(self, x):
    """Generate the JSON for one color from a hex RGB string."""
    d = {}
    d['hex'] = {}
    d['hex']['rgb'] = x
    d['hex']['r'] = comp_hex(x)[0]
    d['hex']['g'] = comp_hex(x)[1]
    d['hex']['b'] = comp_hex(x)[2]
    d['rgb'] = {}
    d['rgb']['r'] = comp_rgb(x)[0]
    d['rgb']['g'] = comp_rgb(x)[1]
    d['rgb']['b'] = comp_rgb(x)[2]
    d['rgb']['rgb'] = 'rgb({}, {}, {})'.format(
      d['rgb']['r'], d['rgb']['g'], d['rgb']['b'])
    d['dec'] = {}
    d['dec']['r'] = '{:.09f}'.format(comp_dec(x)[0])
    d['dec']['g'] = '{:.09f}'.format(comp_dec(x)[1])
    d['dec']['b'] = '{:.09f}'.format(comp_dec(x)[2])
    d['dec']['rgb'] = 'rgb({}, {}, {})'.format(
      d['dec']['r'], d['dec']['g'], d['dec']['b'])
    return d

  def json(self):
    """Generate the JSON for the entire scheme."""
    d = {}
    d['theme'] = self._theme
    for i in range(16):
      d['base{:02x}'.format(i)] = self._json_one(self._base[i])
    for name, i in NAME_TO_BASE.items():
      d[name] = d['base{:02x}'.format(i)]
    d['special'] = d[self._special]
    d['wall'] = self._json_one(self._wall)
    return json.dumps(d, indent=2, sort_keys=True)

parser = argparse.ArgumentParser(description='Generate color schemes')
parser.add_argument('colorscheme', type=str,
  help='Name of the colorscheme to generate')
parser.add_argument('special', choices=[
    'black', 'white', 'red', 'orange', 'yellow',
    'green', 'cyan', 'blue', 'pink', 'purple',
  ], help='Name of the special color')
args = parser.parse_args()

# Get the path to a colorscheme relative to this file
filename = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  args.colorscheme + '.json')

print(Scheme(filename, args.special).json())
