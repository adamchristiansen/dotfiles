evaluate-commands %sh{
  plugins="$kak_config/plugins"
  if [ ! -z "$XDG_DATA_HOME" ]; then
    plugins="$XDG_DATA_HOME/kakoune_plugins"
  else
    plugins="$HOME/.local/share/kakoune_plugins"
  fi
  mkdir -p "$plugins"
  if [ ! -e "$plugins/plug.kak" ]; then
    git clone -q "https://github.com/andreyorst/plug.kak.git" "$plugins/plug.kak"
  fi
  printf "%s\n" "source '$plugins/plug.kak/rc/plug.kak'"
}
plug "andreyorst/plug.kak" noload

plug "adamchristiansen/kakclip" config %{
  kakclip-enable
}

plug "andreyorst/fzf.kak" config %{
  map global user <a-c> ":fzf-cd<ret>" -docstring "change directory"
  map global user b ":fzf-buffer<ret>" -docstring "change buffer"
  map global user <a-b> ":fzf-delete-buffer<ret>" -docstring "delete buffer"
  map global user e ":fzf-vcs<ret>" -docstring "edit file in vcs repo"
  map global user f ":fzf-file<ret>" -docstring "open file"
  map global user F ":fzf-file buffile-dir<ret>" -docstring "open file relative to current buffer"
  map global user g ":fzf-grep<ret>" -docstring "grep file contents recursively"
  map global user s ":fzf-buffer-search<ret>" -docstring "search in buffer"
  map global user z ":fzf-mode<ret>" -docstring "fzf user mode"
} demand fzf %{
  require-module fzf-buffer
  require-module fzf-cd
  require-module fzf-file
  require-module fzf-grep
  require-module fzf-search
  require-module fzf-vcs
} config %{
  set-option global fzf_file_command "fd"
  set-option global fzf_grep_command "rg"
  set-option global fzf_highlight_command "bat"

  set-option global fzf_default_opts %sh{ printf "$FZF_DEFAULT_OPTS" }
  set-option global fzf_preview true
  set-option global fzf_preview_height '50%'
  set-option global fzf_preview_width '50%'
  set-option global fzf_preview_pos "right"

  set-option global fzf_preview_tmux_height '70%'
  set-option global fzf_tmux_height '70%'
  set-option global fzf_tmux_popup true
  set-option global fzf_tmux_popup_width '70%'

  set-option global fzf_horizontal_map "ctrl-s"
  set-option global fzf_vertical_map "ctrl-v"
  set-option global fzf_window_map "ctrl-w"
}

plug "andreyorst/smarttab.kak"

plug "https://gitlab.com/Screwtapello/kakoune-inc-dec"
