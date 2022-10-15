# Integration with tmux.

define-command -hidden tmux-horizontal -params .. %{
  evaluate-commands %{
    tmux-terminal-vertical kak -c %val{session} -e "%arg{@}"
  }
}

define-command -hidden tmux-vertical -params .. %{
  evaluate-commands %{
    tmux-terminal-horizontal kak -c %val{session} -e "%arg{@}"
  }
}

define-command -hidden tmux-window -params .. %{
  evaluate-commands %{
    tmux-terminal-window kak -c %val{session} -e "%arg{@}"
  }
}

define-command -hidden tmux-popup -params .. %{
  nop %sh{
    # $@ is separated by newlines so it is first properly quoted
    args=""
    first=true
    for x; do
      if [ "$first" = true ]; then
        args="$x"
        first=false
      else
        args="$args %{$x}"
      fi
    done
    tmux popup -E -t "$kak_client_env_TMUX_PANE" \
      -w "$kak_opt_fzf_tmux_width" -h "$kak_opt_fzf_tmux_height" \
      env kak -c "$kak_session" -e "$args" \
      < /dev/null > /dev/null 2>&1 &
  }
}
