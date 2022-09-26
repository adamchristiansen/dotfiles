# Magic Shell

Automatically load variables, aliases, and abbreviations using `magic-enviro`,
`magic-alias`, and `magic-abbr`.

## Enviro

Environment variables in _enviro_ format are defined in the following way:

- They must go in a file with a `.enviro` extension.
- All `*.enviro` files in this directory are loaded in lexicographical order.
- Empty lines are allowed.
- Lines containing only comments (`# ...`) are allowed.
  - Comments are not allowed on the same line as a variable definition.
- Variable/alias/abbreviation values can be unquoted (if just a single token),
  single quoted, or double quoted.
- Lines matching the form `export VAR=...` are allowed, and the variables are
  exported.
- Lines matching the form `VAR=...` are allowed, and the variables are
  treated as local and used only in the file.
- Variable values can be single quoted, double quoted, or unquoted.
- Variable interpolation is allowed, with
  - `$VAR` and `${VAR}` forms are supported.
  - Variables are not interpolated within single quote strings.
- All files matching `$HOME/.local/etc/enviro.d/*.enviro` are loaded.

> **Note**: `enviro` is a non-standard environment variable format conceived
> by me for the purpose of these dotfiles.
