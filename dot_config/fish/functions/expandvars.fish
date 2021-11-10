function expandvars \
        --description="Expand variables in a string" \
        --no-scope-shadowing

    # Since this function is executed in the calling scope, all variables
    # declared in this function as severely mangled in the hope that they
    # do not conflict with anything in the parent scope.
    # These are mangled by prefixing with:
    #
    #   __expandvars_

    # The string to expand is all of the arguments separated by a space
    set __expandvars_s "$argv"

    # Get a copy of the original string to expand
    set __expandvars_e $s

    # Extract the names of the variables in the string and set them to
    # themselves. This is necessary because fish expands variables as a
    # Cartesian product, so for example, if "$x:a" is the input and $x is
    # undefined, then when fish expands the expression it will result in an
    # empty string, when we really want the result ":a". To get around this,
    # the variables are first expanded to themselves, so if they are undefined
    # they are set to an empty string.
    while true
        # Break when there are no more variables to consider
        if echo $__expandvars_e | sed -En '/^.*\$([a-zA-Z_0-9]+).*$/{q1};{q0}'
            break
        end
        # Extract the variable name and set it to itself
        set __expandvars_v \
            (echo $__expandvars_e | sed -E 's/^.*\$([a-zA-Z_0-9]+).*$/\1/')
        set $__expandvars_v (eval echo \$$__expandvars_v)
        # Remove all instances of the variable from the original string
        set __expandvars_e \
            (echo $__expandvars_e | sed -E "s/\\\$$__expandvars_v//g")
    end

    # Evaluate the final string
    eval "echo \"$__expandvars_s\""

    # Delete the function variables so that they do not persist in the parent scope
    set -e __expandvars_e
    set -e __expandvars_s
    set -e __expandvars_v

    return 0
end
