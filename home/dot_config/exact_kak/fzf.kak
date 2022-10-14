declare-option str fzf_preview_height '50%'
declare-option str fzf_preview_width '50%'
declare-option str fzf_preview_position 'top'

declare-option str fzf_tmux_height '66%'
declare-option str fzf_tmux_width '75%'

define-command fzf -hidden -params .. %{
  evaluate-commands %sh{
    # Parse the arguments to the command
    directory="$PWD"
    items_command='ls'
    filter_command=''
    preview='false'
    transform_command=''
    kak_command='nop'
    while [ $# -gt 0 ]; do
      case $1 in
        -directory) directory="$2" ;;
        -items)     items_command="$2" ;;
        -filter)    filter_command="$2" ;;
        -preview)   preview="$2" ;;
        -transform) transform_command="$2" ;;
        -kak)       kak_command="$2" ;;
      esac
      shift
      shift
    done

    # Determine the preview dimensions
    preview_window=
    case $kak_opt_fzf_preview_position in
      left|right)
        preview_window="$kak_opt_fzf_preview_position:$kak_opt_fzf_preview_width"
        ;;
      top|bottom)
        preview_window="$kak_opt_fzf_preview_position:$kak_opt_fzf_preview_height"
        ;;
      *)
        preview_window="right:$kak_opt_fzf_preview_width"
        ;;
    esac

    # Create a temporary script to run asynchronously
    tmp_script="$(mktemp "${TMPDIR:-/tmp}/kakoune.fzf.XXXXXXXX")"
    chmod a+x "$tmp_script"

    # Build the fzf script
    (
      # Attempt to add a shebang line to the top of the script. If sh is not
      # found, the script will ikely work anyway since ancient unix magic is
      # used to run the script as a shell script for the currently running
      # shell (which is sh).
      shell="$(type -p sh)"
      if [ -z "$shell" ]; then
        shell="/bin/sh"
      fi
      printf "%s\n" "#!$shell"

       # The shell is exported so that fzf can use it for the preview
      printf "%s\n" "export SHELL='$shell'"

      # Change to the current directory of kakoune
      printf "%s\n" "cd '$directory'"

      # Use fzf to get data to process
      printf "%s" "$items_command"
      if [ -n "$filter_command" ]; then
        printf " | %s" "$filter_command"
      fi
      printf " | %s" "fzf --border=none --height=100%"
      if [ "$preview" = "true" ]; then
        printf " %s" "--preview 'bat --color=always --style=plain {}'"
        printf " %s" "--preview-window=$preview_window"
      fi
      if [ -n "$transform_command" ]; then
        printf " | %s" "$transform_command"
      fi

      # Send the commands to the kakoune session
      printf "%s\n" " | while read line; do"
      printf "  printf '%%s\\\n' \"eval -client %%{%s} %s %%{\$line}\"" \
        "$kak_client" "$kak_command"
      printf "%s\n" " | kak -p '$kak_session'"
      printf "%s\n" "done"

      # Delete this script
      printf "%s\n" "rm -f '$tmp_script'"
    ) > "$tmp_script"

    # Show fzf in a tmux popup to make a selection
    if [ -n "$kak_client_env_TMUX" ]; then
      printf "%s\n" "nop %sh{
        command tmux popup -E -t '$kak_client_env_TMUX_PANE' \
        -w '$kak_opt_fzf_tmux_width' -h '$kak_opt_fzf_tmux_height' \
        env $tmp_script \
        < /dev/null > /dev/null 2>&1 & }" > "$kak_command_fifo"
    else
      # Not in tmux so delete the script
      rm -f "$tmp_script"
    fi
  }
}

define-command fzf-buffer -hidden %{
  evaluate-commands %sh{
    buffers=""
    eval "set -- $kak_quoted_buflist"
    for x; do
      buffers="$(printf "%s\n%s" "$x" "$buffers")"
    done
    printf "fzf"
    printf " -directory %%{%s}" "$PWD"
    printf " -items %%{%s}"     "printf '%s\n' '$buffers'"
    printf " -filter %%{%s}"    "grep -vE '^\*.*\*\$'"
    printf " -preview %%{%s}"   "true"
    printf " -transform %%{%s}" ""
    printf " -kak %%{%s}"       "edit -existing"
  }
}

define-command fzf-buffer-delete -hidden %{
  evaluate-commands %sh{
    buffers=""
    eval "set -- $kak_quoted_buflist"
    for x; do
      buffers="$(printf "%s\n%s" "$x" "$buffers")"
    done
    printf "fzf"
    printf " -directory %%{%s}" "$PWD"
    printf " -items %%{%s}"     "printf '%s\n' '$buffers'"
    printf " -filter %%{%s}"    "grep -vE '^\*.*\*\$'"
    printf " -preview %%{%s}"   "true"
    printf " -transform %%{%s}" ""
    printf " -kak %%{%s}"       "delete-buffer"
  }
}

define-command fzf-cd -hidden %{
  evaluate-commands %sh{
    d="$PWD/.."
    printf "fzf"
    printf " -directory %%{%s}" "$d"
    printf " -items %%{%s}"     "fd --strip-cwd-prefix --hidden --ignore-vcs --type d"
    printf " -filter %%{%s}"    ""
    printf " -preview %%{%s}"   "false"
    printf " -transform %%{%s}" "{ while read x; do printf '%s\n' \"$d/\$x\"; done }"
    printf " -kak %%{%s}"       "cd"
  }
}

define-command fzf-file -hidden %{
  evaluate-commands %sh{
    printf "fzf"
    printf " -directory %%{%s}" "$PWD"
    printf " -items %%{%s}"     "fd --strip-cwd-prefix --hidden --ignore-vcs --type f"
    printf " -filter %%{%s}"    ""
    printf " -preview %%{%s}"   "true"
    printf " -transform %%{%s}" ""
    printf " -kak %%{%s}"       "edit"
  }
}

define-command fzf-file-git -hidden %{
  evaluate-commands %sh{
    if [ "$(git rev-parse --is-inside-work-tree)" = true ]; then
      root="$(git rev-parse --show-toplevel)"
      printf "fzf"
      printf " -directory %%{%s}" "$root"
      printf " -items %%{%s}"     "git ls-tree --full-tree --name-only -r HEAD"
      printf " -filter %%{%s}"    ""
      printf " -preview %%{%s}"   "true"
      printf " -transform %%{%s}" "{ while read x; do printf '%s\n' \"$root/\$x\"; done }"
      printf " -kak %%{%s}"       "edit"
    else
      printf "fzf-file"
    fi
  }
}

define-command fzf-file-relative-to-buffer -hidden %{
  evaluate-commands %sh{
    d="$(dirname "$kak_buffile")"
    printf "fzf"
    printf " -directory %%{%s}" "$d"
    printf " -items %%{%s}"     "fd --strip-cwd-prefix --hidden --ignore-vcs --type f"
    printf " -filter %%{%s}"    ""
    printf " -preview %%{%s}"   "true"
    printf " -transform %%{%s}" "{ while read x; do printf '%s\n' \"$d/\$x\"; done }"
    printf " -kak %%{%s}"       "edit"
  }
}
