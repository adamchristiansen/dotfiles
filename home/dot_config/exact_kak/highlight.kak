# Custom highlighters.

# Defaults.
hook global BufCreate .* %{
  add-highlighter buffer/ number-lines \
    -relative -hlcursor -separator '  ' -min-digits 4
  add-highlighter buffer/ show-matching
  add-highlighter buffer/ show-whitespaces \
    -lf ' ' -spc ' ' -nbsp '~' -tab '›' -tabpad '·' -indent '┊'
  add-highlighter buffer/trailing-whitespaces regex "(\h+)$" 1:Error
}

# Text wrapping.
declare-option -hidden bool highlight_wrap_enabled false
define-command -hidden highlight-wrap-toggle %{
  evaluate-commands %sh{
    if [ "$kak_opt_highlight_wrap_enabled" = 'true' ]; then
      printf "highlight-wrap-disable\n"
    else
      printf "highlight-wrap-enable\n"
    fi
  }
}
define-command -hidden highlight-wrap-enable %{
  add-highlighter -override buffer/wrap wrap -word -indent -marker ''
  set-option buffer highlight_wrap_enabled true
}
define-command -hidden highlight-wrap-disable %{
  remove-highlighter buffer/wrap
  set-option buffer highlight_wrap_enabled false
}
