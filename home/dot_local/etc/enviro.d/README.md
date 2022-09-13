## Enviro

To maintain compatibility with non-POSIX shells, environment variables are
defined in the following way:

- Empty lines are allowed
- Lines containing only comments (`# ...`) are allowed
  - Comments are not allowed on the same line as a variable definition
- Variable/alias/abbreviation values can be unquoted (if just a single token),
  single quoted, or double quoted
- Lines matching the form `export VAR=...` are allowed, and the variables are
  exported
- Lines matching the form `VAR=...` are allowed, and the variables are
  treated as local and used only in the file
- Simple variable interpolation like `$VAR` is allowed
  - No other interpolations are allowed (like `${VAR}` and `${VAR:...}`)
  - Variables are not interpolated within single quote strings
- All files matching `$HOME/.local/etc/enviro.d/*.enviro` are loaded.

> **Note**: `enviro` is a non-standard environment variable format conceived by
> me for the purpose of these dotfiles.
