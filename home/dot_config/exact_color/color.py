#!/usr/bin/env python3

import argparse
import json
import os

# Maps a name to base color for named colors.
NAMES = {
  'bg':     'base00',
  'black':  'base03',
  'fg':     'base05',
  'white':  'base05',
  'red':    'base08',
  'orange': 'base09',
  'yellow': 'base0a',
  'green':  'base0b',
  'cyan':   'base0c',
  'blue':   'base0d',
  'pink':   'base0e',
  'purple': 'base0f',
}

class Color:
  def __init__(self, hex):
    hex = hex.lower()
    assert len(hex) == 6 and set(hex) <= set('0123456789abcdef')
    self._hex = hex

  @property
  def hex_rgb(self):
    return self._hex
  @property
  def hex_r(self):
    return self._hex[0:2]
  @property
  def hex_g(self):
    return self._hex[2:4]
  @property
  def hex_b(self):
    return self._hex[4:6]

  @property
  def rgb(self):
    return f"rgb({self.r}, {self.g}, {self.b})"
  @property
  def r(self):
    return int(self.hex_r, 16)
  @property
  def g(self):
    return int(self.hex_g, 16)
  @property
  def b(self):
    return int(self.hex_b, 16)

  @property
  def dec_rgb(self):
    return f"rgb({self.dec_r}, {self.dec_g}, {self.dec_b})"
  @property
  def dec_r(self):
    return round(self.r / 255, 9)
  @property
  def dec_g(self):
    return round(self.g / 255, 9)
  @property
  def dec_b(self):
    return round(self.b / 255, 9)

  def blend(self, scale):
    assert -1 <= scale <= 1
    r, g, b = self.dec_r, self.dec_g, self.dec_b
    if scale < 0:
      scale = abs(scale)
      r = (1 - scale) * r
      g = (1 - scale) * g
      b = (1 - scale) * b
    else:
      r = (1 - scale) * r + scale
      g = (1 - scale) * g + scale
      b = (1 - scale) * b + scale
    c = lambda x: int(round(255 * x))
    return Color(f"{c(r):02x}{c(g):02x}{c(b):02x}")

  def blend_to(self, color, scale):
    assert 0 <= scale <= 1
    r, g, b = self.dec_r, self.dec_g, self.dec_b
    cr, cg, cb = color.dec_r, color.dec_g, color.dec_b
    r = (1 - scale) * r + scale * cr
    g = (1 - scale) * g + scale * cg
    b = (1 - scale) * b + scale * cb
    c = lambda x: int(round(255 * x))
    return Color(f"{c(r):02x}{c(g):02x}{c(b):02x}")

  def json(self):
    return {
      'hex': {
        'rgb': self.hex_rgb,
        'r': self.hex_r,
        'g': self.hex_g,
        'b': self.hex_b,
      },
      'rgb': {
        'rgb': self.rgb,
        'r': str(self.r),
        'g': str(self.g),
        'b': str(self.b),
      },
      'dec': {
        'rgb': self.dec_rgb,
        'r': str(self.dec_r),
        'g': str(self.dec_g),
        'b': str(self.dec_b),
      },
    }

class Scheme:
  def __init__(self, filename, special):
    # Load the data from a file
    with open(filename) as f:
      data = json.load(f)

    # Theme.
    self._theme = data['theme']
    assert self._theme in ['light', 'dark']

    # Base colors.
    #
    # These are parallel arrays of basename and color.
    self._bases = sorted([k for k in data.keys() if k.startswith('base')])
    self._base_colors = [Color(data[base]) for base in self._bases]
    assert self._bases == [f"base{i:02x}" for i in range(16)]

    # Wall color.
    self._wall = Color(data['wall'])

    # Blending.
    self._bg_blend      = float(data['bg_blend'])
    self._soft_bg_blend = float(data['soft_bg_blend'])
    self._soft_fg_blend = float(data['soft_fg_blend'])
    self._fg_blend      = float(data['fg_blend'])
    assert 0 <= self._bg_blend <= 1
    assert 0 <= self._soft_bg_blend <= 1
    assert 0 <= self._soft_fg_blend <= 1
    assert 0 <= self._fg_blend <= 1

    # Special color name.
    assert special in NAMES.keys()
    self._special = special

  def json(self):
    d = {}
    d['theme'] = self._theme
    c = {} # Maps color name to `Color` object.
    # Base colors.
    for base, color in zip(self._bases, self._base_colors):
      c[base] = color
      d[base] = color.json()
      # d[f"{base}_bg"] = color.blend_to(bg, self._bg_blend).json()
    # Named colors.
    for name, base in NAMES.items():
      c[name] = c[base]
      d[name] = d[base]
    # Special color.
    c['special'] = c[self._special]
    d['special'] = d[self._special]
    # Wall color.
    c['wall'] = self._wall
    d['wall'] = self._wall.json()
    # Blend colors.
    bg = c[NAMES['bg']]
    fg = c[NAMES['fg']]
    for name in list(c.keys()):
      color = c[name]
      c[f"{name}_bg"]      = color.blend_to(bg, self._bg_blend)
      c[f"{name}_soft_bg"] = color.blend_to(bg, self._soft_bg_blend)
      c[f"{name}_soft_fg"] = color.blend_to(fg, self._soft_fg_blend)
      c[f"{name}_fg"]      = color.blend_to(fg, self._fg_blend)
      d[f"{name}_bg"]      = c[f"{name}_bg"].json()
      d[f"{name}_soft_bg"] = c[f"{name}_soft_bg"].json()
      d[f"{name}_soft_fg"] = c[f"{name}_soft_fg"].json()
      d[f"{name}_fg"]      = c[f"{name}_fg"].json()
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
