function sourceprofile -a file \
        --description="Source environment export statements"

    # A file name argument must be supploed and it must exist
    if [ -z "$file" -o  ! -f "$file" ]
        return 1
    end

    cat $file | while read expr
        set -l expr (string trim $expr)

        # Ignore empty lines and comments
        if [ -z "$expr" ] || string match -q '#*' $expr
            continue
        end

        if string match -q 'export *' $expr
            # Get the variable name and value
            set -l var   (echo $expr | sed -E "s/^export ([a-zA-Z_][a-zA-Z_0-9]+)=(.*)\$/\1/")
            set -l value (echo $expr | sed -E "s/^export ([a-zA-Z_][a-zA-Z_0-9]+)=(.*)\$/\2/")
            # Remove surrounding quotes (if any)
            set value (echo $value | sed -E "s/^\"(.*)\"\$/\1/")
            # Export the variable
            if [ $var = "PATH" ]
                # Split the components of the path, and add each path to
                # $fish_user_paths. The order of whether the paths are
                # prepended or appended to the $PATH are not preserved. They
                # will be added to $fish_user_paths in the order they appear
                # in the file
                for v in (string split ":" $value)
                    if [ $v != "\$PATH" ]
                        # Expand the path in case it contains $HOME, and only
                        # add the path if it does not already exist.
                        set -l path (eval echo $v)
                        if not contains $path $PATH \
                                && not contains $path $fish_user_paths
                            set -Ua fish_user_paths $path
                        end
                    end
                end
            else
                set -gx $var (eval echo $value)
            end
        else
            # Get the variable name and value
            set -l var   (echo $expr | sed -E "s/^([a-zA-Z_][a-zA-Z_0-9]+)=(.*)\$/\1/")
            set -l value (echo $expr | sed -E "s/^([a-zA-Z_][a-zA-Z_0-9]+)=(.*)\$/\2/")
            # Remove surrounding quotes (if any)
            set value (echo $value | sed -E "s/^\"(.*)\"\$/\1/")
            # Assign the variable in function scope so that it can be used in
            # other variables
            set $var (eval echo $value)
        end
    end
end
