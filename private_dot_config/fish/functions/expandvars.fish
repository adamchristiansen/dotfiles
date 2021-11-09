function expandvars --description="Expand variables in a string"
    # The string to expand is all of the arguments separated by a space
    set s "$argv"

    # Get a copy of the original string to expand
    set e $s

    # Extract the names of the variables in the string and set them to
    # themselves. This is necessary because fish expands variables as a
    # Cartesian product, so for example, if "$x:a" is the input and $x is
    # undefined, then when fish expands the expression it will result in an
    # empty string, when we really want the result ":a". To get around this,
    # the variables are first expanded to themselves, so if they are undefined
    # they are set to an empty string.
    while true
        # Break when there are no more variables to consider
        if echo $e | sed -E '/^.*\$([a-zA-Z_0-9]+).*$/{q100};{q0}' > /dev/null
            break
        end
        # Extract the variable name and set it to itself
        set v (echo $e | sed -E 's/^.*\$([a-zA-Z_0-9]+).*$/\1/')
        set $v (eval echo \$$v)
        # Remove all instances of the variable from the original string
        set e (echo $e | sed -E "s/\\\$$varname//g")
    end

    # Evaluate the final string
    eval echo $s
end
