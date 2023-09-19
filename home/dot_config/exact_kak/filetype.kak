# Set custom filetype associations.

hook global BufCreate .*\.bib %{
  set buffer filetype latex
}
