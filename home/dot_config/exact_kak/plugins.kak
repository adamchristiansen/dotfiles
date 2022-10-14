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

plug "andreyorst/smarttab.kak"
