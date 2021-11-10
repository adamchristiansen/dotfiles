evaluate-commands %sh{
    plugins="$kak_config/plugins"
    mkdir -p "$plugins"
    if [ ! -e "$plugins/plug.kak" ]; then
        git clone -q https://github.com/andreyorst/plug.kak.git "$plugins/plug.kak"
    fi
    printf "%s\n" "source '$plugins/plug.kak/rc/plug.kak'"
}
plug "andreyorst/plug.kak" noload

plug "AdamChristiansen/kakclip" config %{
    kakclip-enable
}

plug "andreyorst/kaktree" defer kaktree %{
    define-command -hidden kaktree-show-focus %{ evaluate-commands %sh{
        if [ "${kak_opt_kaktree__active}" = "true" ]; then
            if [ "${kak_opt_kaktree__onscreen}" = "true" ]; then
                printf "%s\n" "kaktree-focus"
            else
                printf "%s\n" "kaktree-toggle"
            fi
        fi
    }}

    map global user f :kaktree-show-focus<ret> \
        -docstring "show and focus file tree"
    map global user "F" ":kaktree-toggle<ret>" -docstring "toggle file tree"

    set-option global kaktree_dir_icon_close "▸  "
    set-option global kaktree_dir_icon_open  "▾  "
    set-option global kaktree_file_icon      "⠀⠀ "
    set-option global kaktree_indentation 2
    set-option global kaktree_show_help false
    set-option global kaktree_show_hidden true
    set-option global kaktree_side left
    set-option global kaktree_size 39
    set-option global kaktree_sort true
    set-option global kaktree_split horizontal
} config %{
    hook global WinSetOption filetype=kaktree %{
        remove-highlighter buffer/numbers
        remove-highlighter buffer/matching
        remove-highlighter buffer/wrap
        remove-highlighter buffer/show-whitespaces

        # Hide statusbar
        set-option buffer modelinefmt ''
    }
    kaktree-enable
}

plug "andreyorst/smarttab.kak" defer smarttab %{
    set-option global softtabstop 4
} config %{
    # By default, do not expand tabs. If tabs are used they are to be
    # overridden explicitly
    hook global WinSetOption filetype=.*       expandtab
    hook global WinSetOption filetype=makefile noexpandtab
}
