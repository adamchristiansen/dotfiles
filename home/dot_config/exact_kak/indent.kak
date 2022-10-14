# Define the behaviour of tabs and indents.

define-command -hidden indent-config %{
  evaluate-commands %sh{
    if [ "$kak_opt_aligntab" = true -o "$kak_opt_indentwidth" -eq 0 ]; then
      printf "indent-config-noexpand\n"
    else
      printf "indent-config-expand\n"
    fi
  }
}

define-command -hidden indent-config-expand %{
  set-option buffer aligntab false
  remove-hooks buffer indent-config
  # Replace the tab key with an appropriate number of spaces
  hook -group indent-config buffer InsertChar '\t' %{
    execute-keys -draft "h%opt{indentwidth}@"
  }
}

define-command -hidden indent-config-noexpand %{
  set-option buffer aligntab true
  set-option buffer indentwidth 0
  remove-hooks buffer indent-config
}
