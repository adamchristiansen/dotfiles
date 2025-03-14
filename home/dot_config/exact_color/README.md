# Color

This document describes how colors are configured for use in `chezmoi`
templates.



## Color Semantics

Color themes are defined using the
[`base16`](https://github.com/chriskempson/base16) semantics, which are

- `base00`: default background
- `base01`: lighter background (used for status bars)
- `base02`: selection background
- `base03`: comments, invisibles, line highlighting
- `base04`: dark foreground (used for status bars)
- `base05`: default foreground, caret, delimiters, operators
- `base06`: light foreground (not often used)
- `base07`: light background (not often used)
- `base08`: variables, XML tags, markup link text, markup lists, diff deleted
- `base09`: integers, boolean, constants, XML attributes, markup link URL
- `base0a`: classes, markup bold, search text background
- `base0b`: strings, inherited class, markup code, diff inserted
- `base0c`: support, regular expressions, escape characters, markup quotes
- `base0d`: functions, methods, attribute IDs, headings
- `base0e`: keywords, storage, selector, markup italic, diff changed
- `base0f`: deprecated, opening/closing embedded language tags

In addition, some of the `base16` colors are treated in following way:

- `base03`: Black
- `base05`: White
- `base08`: Red
- `base09`: Orange
- `base0a`: Yellow
- `base0b`: Green
- `base0c`: Cyan
- `base0d`: Blue
- `base0e`: Pink
- `base0f`: Purple

It is not necessary for `base08` to be specified as red, however, it will be
used with _red semantics_.

The following aliases are defined that can be used:

- `bg` → `base00`
- `black` → `base03`
- `fg` → `base05`
- `white` → `base05`
- `red` → `base08`
- `orange` → `base09`
- `yellow` → `base0a`
- `green` → `base0b`
- `cyan` → `base0c`
- `blue` → `base0d`
- `pink` → `base0e`
- `purple` → `base0f`
- `special` → The `specialColor` in the chezmoi data

The `special` color should be used as an accent color.

In addition to the 16 colors above, an additional color called `wall` is
defined, which is the fallback color for wallpapers.

Every color also has a background and foreground variants with specific suffixes on the name.

- `_bg`: Strongly blended toward `base00` (i.e., `bg`).
- `_soft_bg`: Weakly blended toward `base00` (i.e., `bg`).
- `_soft_fg`: Weakly blended toward `base05` (i.e., `fg`).
- `_fg`: Strongly blended toward `base05` (i.e., `fg`).



## Generating Colors

Each color scheme should go in a file named `<colorscheme>.json`, where
`<colorscheme>` is the name of the color scheme. These files should contain the
following JSON:

```json
{
  "theme": "theme_type",
  "base00": "xxxxxx",
  "base01": "xxxxxx",
  "base02": "xxxxxx",
  "base03": "xxxxxx",
  "base04": "xxxxxx",
  "base05": "xxxxxx",
  "base06": "xxxxxx",
  "base07": "xxxxxx",
  "base08": "xxxxxx",
  "base09": "xxxxxx",
  "base0a": "xxxxxx",
  "base0b": "xxxxxx",
  "base0c": "xxxxxx",
  "base0d": "xxxxxx",
  "base0e": "xxxxxx",
  "base0f": "xxxxxx",
  "wall": "xxxxxx",
  "bg_blend": blend,
  "bg_soft_blend": blend,
  "fg_soft_blend": blend,
  "fg_blend": blend,
}
```

where

- `theme_type` is either `dark` or `light`. This is used by some applications
  for additional context on how the colors should be applied. Use `dark` for
  themes with a `dark` beckground and vice versa.
- `xxxxxx` is a color specified in hexadecimal RGB (without a leading `#`).
- `blend` is a number in [0, 1].

For blending, the setting indicates how much each color is blended with a
reference to produce a color variant. When the blend is 0, then the original
color is kept, and when the blend is 1, then the reference color is taken. A
fractional blending is a linear interpolation in RGB space between the colors.



## Color Variables

When `chezmoi` runs, it generates a file called `.color.json`, which has the
full color scheme definition. To access these values from a `chezmoi` template,
include the following line in the template file:

```
{{- $color := includeTemplate "color.json" . | mustFromJson -}}
```

This gives access to the following:

- `$color.theme` is either `dark` or `light`.
- `$color.<name>.<format>.<value>` is the color value, where:
  - `<name>` can be `base00` through `base0f` or `wall`
  - `<format>` can be
    - `hex` for 24-bit hexadecimal values
    - `rgb` for 24-bit decimal values
    - `dec` for fractional decimal color values between `0.0` and `1.0`
  - `<value>` can be:
    - `r` for the red component
    - `g` for the green component
    - `b` for the blue component
    - Additionally, for `hex` formats the following are defined:
      - `rgb` is the traditional hex format with 6 hex characters
    - Additionally, for `rgb` formats the following are defined:
      - `rgb` is `rgb(r, g, b)` where `r`, `g`, `b` are 0 to 255
    - Additionally, for `dec` formats the following are defined:
      - `rgb` is `rgb(r, g, b)` where `r`, `g`, `b` are 0 to 1

Here are some examples:

```css
/*
Use the full hex format. Remember that the `#` is
not included so it must be include manually.
*/
.wallpaper {
  background: #{{ $color.wall.hex.rgb }};
}

/*
Use a decimal RGB format.
*/
.text {
  color: rgb(
    {{- $color.base0b.rgb.r -}},
    {{- $color.base0b.rgb.g -}},
    {{- $color.base0b.rgb.b -}});
}
```

## Themes

The following themes are available:

- `moonlight`: a custom medium contrast dark color scheme
- `seaside`: a custom low contrast dark color scheme
