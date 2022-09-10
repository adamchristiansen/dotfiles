declare-option -hidden str modeline_modified
define-command -hidden modeline-update-modified %{
  set-option buffer modeline_modified %sh{
    if [ "$kak_modified" = true ]; then
      printf "%s \n" "●"
    else
      printf "\n"
    fi
  }
}

declare-option -hidden str modeline_readonly
define-command -hidden modeline-update-readonly %{
  set-option buffer modeline_readonly %sh{
    if [ "$kak_opt_readonly" = true -o ! -w "$kak_buffile" ]; then
      printf "%s \n" ""
    else
      printf "\n"
    fi
  }
}

declare-option -hidden str modeline_selections
define-command -hidden modeline-update-selections %{
  set-option buffer modeline_selections %sh{
    printf "%s\n" $(echo "$kak_selections_length" | wc -w | sed 's/[ \t]//g')
  }
}

define-command -hidden modeline-update-all %{
  modeline-update-modified
  modeline-update-readonly
  modeline-update-selections
}

define-command -hidden modeline-update-idle %{
  modeline-update-modified
  modeline-update-selections
}

define-command -hidden modeline-bufname-setup-hooks %{
  remove-hooks global modeline-bufname
  hook -group modeline-bufname global BufWritePost .* %{ modeline-update-all }
  hook -group modeline-bufname global BufSetOption readonly=.+ %{ modeline-update-readonly }
  hook -group modeline-bufname global WinDisplay .* %{ modeline-update-all }

  hook -group modeline-bufname global InsertIdle .* %{ modeline-update-idle }
  hook -group modeline-bufname global NormalIdle .* %{ modeline-update-idle }
  hook -group modeline-bufname global PromptIdle .* %{ modeline-update-idle }
}

declare-option -hidden bool modeline_enabled true
define-command -docstring "enable modeline" modeline-enable %{
  set-option global modeline_enabled true
  set-option global modelinefmt '{StatusLineValue}%opt{modeline_modified}{StatusLineInfo}%opt{modeline_readonly}%val{bufname} 視%opt{modeline_selections} ﳗ %val{cursor_line}:%val{cursor_char_column} 歷%val{client}‧%val{session}'
  modeline-bufname-setup-hooks
}
define-command -docstring "disable modeline" modeline-disable %{
  set-option global modeline_enabled false
  set-option global modelinefmt ''
  remove-hooks global modeline-bufname
}
define-command -docstring "toggle modeline" modeline-toggle %{
  evaluate-commands %sh{
    if [ "$kak_opt_modeline_enabled" = true ]; then
      printf "%s\n" "modeline-disable"
    else
      printf "%s\n" "modeline-enable"
    fi
  }
}

modeline-enable
