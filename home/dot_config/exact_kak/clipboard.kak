# System clipboard integration using the clipboard command.

define-command -hidden clipboard-paste-after %{
  evaluate-commands %sh{
    printf "%s\n" "execute-keys -draft '<a-!>clipboard --paste<ret>'"
  }
}

define-command -hidden clipboard-paste-before %{
  evaluate-commands %sh{
    printf "%s\n" "execute-keys -draft '!clipboard --paste<ret>'"
  }
}

define-command -hidden clipboard-replace %{
  evaluate-commands %sh{
    printf "execute-keys -draft %%{| %s; %s<ret>}\n" \
      "printf '' > /dev/null 2>&1" \
      "clipboard --paste"
  }
}

define-command -hidden clipboard-yank-buffer %{
  execute-keys -draft '%:clipboard-yank-selection<ret>'
}

define-command -hidden clipboard-yank-selection %{
  nop %sh{
    printf "%s" "$kak_main_reg_dot" | clipboard --copy > /dev/null 2>&1
  }
}
