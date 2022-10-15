# Use fzf for interactively making selections.

declare-option str fzf_preview_height '50%'
declare-option str fzf_preview_width '50%'
declare-option str fzf_preview_position 'top'

declare-option str fzf_tmux_height '66%'
declare-option str fzf_tmux_width '75%'

# The following options can be given:
#
# -directory: set working directory of script
# -items: command to produce the items to give to fzf
# -filter: command to filter items before giving to fzf
# -preview: show a file preview in fzf
# -transform: command transform the selected values from fzf
# -kak: the kakoune command to run on each item
# -tmux-window: allow opening values in new tmux windows/panes
define-command fzf -hidden -params .. %{
  evaluate-commands %sh{
    # Parse the arguments to the command
    directory="$PWD"
    items_command='ls'
    filter_command=''
    preview='false'
    transform_command=''
    command='nop'
    tmux_window='false'
    while [ $# -gt 0 ]; do
      case $1 in
        -directory)   directory="$2" ;;
        -items)       items_command="$2" ;;
        -filter)      filter_command="$2" ;;
        -preview)     preview="$2" ;;
        -transform)   transform_command="$2" ;;
        -kak)         command="$2" ;;
        -tmux-window) tmux_window="$2" ;;
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
      shell="$(command -v sh)"
      if [ -z "$shell" ]; then
        shell="/bin/sh"
      fi
      printf "%s\n" "#!$shell"

       # The shell is exported so that fzf can use it for the preview
      printf "%s\n" "export SHELL='$shell'"

      # Change to the current directory of kakoune
      printf "%s\n" "cd '$directory'"

      # Tracks whether the first line has been processed
      printf "%s\n" "first=true"

      # The mode for opening the files
      printf "%s\n" "mode=default"

      # Use fzf to get data to process
      printf "%s | \\\\\n" "$items_command"
      if [ -n "$filter_command" ]; then
        printf "%s | \\\\\n" "$filter_command"
      fi
      printf "%s" "fzf --border=none --height=100%"
      if [ "$preview" = "true" ]; then
        printf " %s" "--preview 'bat --color=always --style=plain {}'"
        printf " %s" "--preview-window=$preview_window"
      fi
      if [ -n "$kak_client_env_TMUX" -a "$tmux_window" = "true" ]; then
        printf " %s" "--expect=return,alt--,alt-\\\\,alt-c,alt-p"
      else
        printf " %s" "--expect=return"
      fi
      printf " | \\\\\n"

      # Transform the command output before running actions
      if [ -n "$transform_command" ]; then
        printf "%s | \\\\\n" "$transform_command"
      fi

      # Send the commands to the kakoune session
      printf "%s\n" \
"while read -r line; do
  if [ \"\$first\" = true ]; then
    case \"\$line\" in
      *alt--)  mode=h ;;
      *alt-\\\\) mode=v ;;
      *alt-c)  mode=w ;;
      *alt-p)  mode=p ;;
    esac
    first=false
    continue
  fi
  if [ -n '$kak_client_env_TMUX' ]; then
    case \"\$mode\" in
      h) printf '%s\\n' \"eval -client %{$kak_client} tmux-horizontal '$command %{\$line}'\" ;;
      v) printf '%s\\n' \"eval -client %{$kak_client} tmux-vertical '$command %{\$line}'\" ;;
      w) printf '%s\\n' \"eval -client %{$kak_client} tmux-window '$command %{\$line}'\" ;;
      p) printf '%s\\n' \"eval -client %{$kak_client} tmux-popup '$command %{\$line}'\" ;;
      *) printf '%s\\n' \"eval -client %{$kak_client} $command %{\$line}\" ;;
    esac
  else
    printf '%s\n' 'nop'
  fi | kak -p '$kak_session'
done"

      # Delete this script
      printf "%s\n" "rm -f '$tmp_script'"
    ) > "$tmp_script"

    # Show fzf in a tmux popup to make a selection
    if [ -n "$kak_client_env_TMUX" ]; then
      printf "%s\n" "nop %sh{
        tmux popup -E -t '$kak_client_env_TMUX_PANE' \
        -w '$kak_opt_fzf_tmux_width' -h '$kak_opt_fzf_tmux_height' \
        env '$tmp_script' \
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
    printf " -directory %%{%s}"   "$PWD"
    printf " -items %%{%s}"       "printf '%s\n' '$buffers'"
    printf " -filter %%{%s}"      "grep -vE '^\*.*\*\$'"
    printf " -preview %%{%s}"     "true"
    printf " -transform %%{%s}"   ""
    printf " -kak %%{%s}"         "edit -existing"
    printf " -tmux-window %%{%s}" "true"
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
    printf " -directory %%{%s}"   "$PWD"
    printf " -items %%{%s}"       "printf '%s\n' '$buffers'"
    printf " -filter %%{%s}"      "grep -vE '^\*.*\*\$'"
    printf " -preview %%{%s}"     "true"
    printf " -transform %%{%s}"   ""
    printf " -kak %%{%s}"         "delete-buffer"
    printf " -tmux-window %%{%s}" "false"
  }
}

define-command fzf-cd -hidden %{
  evaluate-commands %sh{
    d="$PWD/.."
    printf "fzf"
    printf " -directory %%{%s}"   "$d"
    printf " -items %%{%s}"       "fd --strip-cwd-prefix --hidden --ignore-vcs --type d"
    printf " -filter %%{%s}"      ""
    printf " -preview %%{%s}"     "false"
    printf " -transform %%{%s}"   "{ while read -r x; do printf '%s\n' \"$d/\$x\"; done }"
    printf " -kak %%{%s}"         "cd"
    printf " -tmux-window %%{%s}" "false"
  }
}

define-command fzf-file -hidden %{
  evaluate-commands %sh{
    printf "fzf"
    printf " -directory %%{%s}"   "$PWD"
    printf " -items %%{%s}"       "fd --strip-cwd-prefix --hidden --ignore-vcs --type f"
    printf " -filter %%{%s}"      ""
    printf " -preview %%{%s}"     "true"
    printf " -transform %%{%s}"   ""
    printf " -kak %%{%s}"         "edit"
    printf " -tmux-window %%{%s}" "true"
  }
}

define-command fzf-file-git -hidden %{
  evaluate-commands %sh{
    if [ "$(git rev-parse --is-inside-work-tree)" = true ]; then
      root="$(git rev-parse --show-toplevel)"
      printf "fzf"
      printf " -directory %%{%s}"   "$root"
      printf " -items %%{%s}"       "git ls-tree --full-tree --name-only -r HEAD"
      printf " -filter %%{%s}"      ""
      printf " -preview %%{%s}"     "true"
      printf " -transform %%{%s}"   "{ while read -r x; do printf '%s\n' \"$root/\$x\"; done }"
      printf " -kak %%{%s}"         "edit"
      printf " -tmux-window %%{%s}" "true"
    else
      printf "fzf-file"
    fi
  }
}

define-command fzf-file-relative-to-buffer -hidden %{
  evaluate-commands %sh{
    d="$(dirname "$kak_buffile")"
    printf "fzf"
    printf " -directory %%{%s}"   "$d"
    printf " -items %%{%s}"       "fd --strip-cwd-prefix --hidden --ignore-vcs --type f"
    printf " -filter %%{%s}"      ""
    printf " -preview %%{%s}"     "true"
    printf " -transform %%{%s}"   "{ while read -r x; do printf '%s\n' \"$d/\$x\"; done }"
    printf " -kak %%{%s}"         "edit"
    printf " -tmux-window %%{%s}" "true"
  }
}
