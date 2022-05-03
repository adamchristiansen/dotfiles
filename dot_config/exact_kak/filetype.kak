provide-module dotfile %{
    add-highlighter shared/dotfile regions
    add-highlighter shared/dotfile/code default-region group
    add-highlighter shared/dotfile/comment region '(^|\h)\K#' '$' fill comment
}

hook global WinSetOption filetype=dotfile %{
    require-module dotfile
}

hook -group dotfile-highlight global WinSetOption filetype=dotfile %{
    add-highlighter window/dotfile ref dotfile
    hook -once -always window WinSetOption filetype=.* %{
        remove-highlighter window/dotfile
    }
}

hook global BufCreate .*\.gitignore %{
    try %{
        set-option buffer filetype dotfile
    }
}
