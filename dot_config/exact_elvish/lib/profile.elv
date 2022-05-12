use path
use re
use util

fn source { |filepath|
  # These are variables that are declared locally within the profile and are
  # not to be exported
  var variables = [&]

  # These are variables that should be exported into the environment ($E:xxx).
  var exports = [&]

  var @lines = (cat $filepath | to-lines)
  all $lines | each { |line|
    # Skip comments and empty lines
    if (re:match '^\s*(#|$)' $line) {
      continue
    }

    # Match a delcaration expression
    var expand = $false
    var match = $nil
    var @match = (re:find '^(export\s+)?(\S+)=''((?:\\.|[^''\\])*)''$' $line)
    if (util:empty $match) {
      set @match = (re:find '^(export\s+)?(\S+)="((?:\\.|[^"\\])*)"$' $line)
      set expand = $true
    }
    if (util:empty $match) {
      set @match = (re:find '^(export\s+)?(\S+)=(([^\s])*)$' $line)
      set expand = $true
    }
    if (util:empty $match) {
      fail 'Profile syntax error: '$line
    }
    var export = (util:not-empty $match[0][groups][1][text])
    var name = $match[0][groups][2][text]
    var body = $match[0][groups][3][text]

    # Expand the variable body
    if $expand {
      var @finds = (re:find '(^|[^$\\])(\$(\w+))' $body)
      util:reverse $finds | each { |find|
        var start = $find[groups][2][start]
        var end = $find[groups][2][end]
        var name = $find[groups][3]
        set body[$start..$end] = (util:find-env $name[text] &vs=$variables)
      }
    }

    # Add the varibles to the lookup and export lists
    set variables[$name] = $body
    if $export {
      set exports[$name] = $body
    }
  }

  # Add the variables to the environment
  keys $exports | each { |name|
    set-env $name $exports[$name]
  }
}

fn source-dir { |dirpath &recurse=$false|
  if (not (path:is-dir $dirpath)) {
    fail 'Path is not a directory'
  }

  ls $dirpath | each { |item|
    set item = $dirpath/$item
    if (path:is-regular $item) {
      source $item
    } elif (and $recurse (path:is-dir $item)) {
      source-dir $item &recurse=$recurse
    }
  }
}
