# Dotfiles

These are my dotfiles, managed by
[chezmoi](https://github.com/twpayne/chezmoi).



## Naming

Anything in the root directory beginning with `_` is not managed by `chezmoi`
(at least not directly). These directories contain either cached values or
configurations which must be installed manually (because they use `sudo`,
cannot be easily scripted, etc).



## Color Themes

If a `chezmoi` template needs access to colors, then include

```
{{- $color := include "_color/color.json" | mustFromJson -}}
```

at the top of the template. Colors can then be accessed through the `$color`
variable, such as

```
{{ $color.base0a.hex.rgb }}
```

See the [color README](_color/README.md) for more information on using colors.



## Profile

To maintain compatibility with non-POSIX shells, such as Elvish, files like
`.profile` and the contents of `.local/etc/profile.d/*` must adhere to the
following rules:

- Empty lines are allowed
- Lines containing only comments are allowed
  - Comments are not allowed on the same line as a variable definition
- Lines matching the form `export VAR=...` are allowed, and the variables are
  exported
- Lines matching the form `VAR=...` are allowed, and the variables are
  treated as local and used only in the file
- Simple variable interpolation like `$VAR` is allowed
  - No other interpolations are allowed (like `${VAR}` and `${VAR:...}`)

These rules are strict but useful, as they can easily be parsed by any shell.
