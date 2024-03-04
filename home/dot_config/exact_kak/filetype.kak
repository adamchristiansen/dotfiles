# Set custom filetype associations.

hook global BufCreate .*\.bib %{
  set buffer filetype latex
}

hook global BufCreate .*\.mdx %{
  set buffer filetype markdown
}
