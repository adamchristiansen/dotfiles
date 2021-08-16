function __fish_command_not_found_handler --on-event fish_command_not_found
    set -l cmd $argv[1]

    if command -q similar-command-search
        set -l cmds (similar-command-search $cmd --count 5)
        if [ (count $cmds) -gt 0 ]
            printf \
                "Oops, %s%s%s does not exist. Some similar commands are:\n" \
                (set_color -u brred) \
                (string escape -- $cmd) \
                (set_color normal) >&2
            for i in (seq (count $cmds))
                printf "  %s%s%s\n" \
                    (set_color brgreen) \
                    (string escape -- $cmds[$i]) \
                    (set_color normal) >&2
            end
        else
            printf "Oops, %s%s%s does not exist.\n" \
                (set_color -u brred) \
                (string escape -- $cmd) \
                (set_color normal) >&2
        end
    else
        printf "Oops, %s%s%s does not exist.\n" \
            (set_color -u brred) \
            (string escape -- $cmd) \
            (set_color normal) >&2
    end
end
