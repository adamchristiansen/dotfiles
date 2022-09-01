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
{{- $color := include ".gen/color.json" | mustFromJson -}}
```

at the top of the template. Colors can then be accessed through the `$color`
variable, such as

```
{{ $color.base0a.hex.rgb }}
```

See the [color README](dot_config/exact_color/README.md) for more information
on using colors.



## Enviro, Aliases, and Abbreviations

To maintain compatibility with non-POSIX shells, such as Elvish, files like
`.config/enviro` and the contents of `.local/etc/enviro.d/*` must adhere to the
following rules:

- Empty lines are allowed
- Lines containing only comments (`# ...`) are allowed
  - Comments are not allowed on the same line as a variable definition
- Variable/alias/abbreviation values can be unquoted (if just a single token),
  single quoted, or double quoted
- For enviros:
  - Lines matching the form `export VAR=...` are allowed, and the variables are
    exported
  - Lines matching the form `VAR=...` are allowed, and the variables are
    treated as local and used only in the file
  - Simple variable interpolation like `$VAR` is allowed
    - No other interpolations are allowed (like `${VAR}` and `${VAR:...}`)
    - Variables are not interpolated within single quote strings
- For aliases/abbreviations:
  - Lines matching `alias VAR=...` are added as aliases/abbreviations
  - Abbreviations are added as aliases so that shells do not support
    abbreviations may still add them
  - Subshells should use POSIX `$(...)` syntax. When parsed by another shell,
    the syntax will be converted appropriately.

> **Note**: `enviro` is a non-standard environment variable format conceived by
> me for the purpose of these dotfiles.

These rules are strict but useful, as they can easily be parsed by any shell.
