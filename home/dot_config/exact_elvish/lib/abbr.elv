use re
use util

fn new { |name body|
  set edit:small-word-abbr[$name] = $body
}

fn source { |filepath|
  var parsed = []
  var @lines = (cat $filepath | to-lines)
  all $lines | each { |line|
    # Skip comments and empty lines
    if (re:match '^\s*(#|$)' $line) {
      continue
    }

    var @match = (re:find '^alias\s+(\S+)=''((?:\\.|[^''\\])*)''$' $line)
    if (util:empty $match) {
      set @match = (re:find '^alias\s+(\S+)="((?:\\.|[^"\\])*)"$' $line)
    }
    if (util:empty $match) {
      set @match = (re:find '^alias\s+(\S+)=(([^\s])*)$' $line)
    }
    if (util:empty $match) {
      fail 'Abbreviation syntax error: '$line
    }
    var name = $match[0][groups][1][text]
    var body = $match[0][groups][2][text]
    # Expand $(...) -> (...)
    set body = (re:replace '\$\(' '(' $body)
    new $name $body
  }
}

fn list {
  keys $edit:small-word-abbr | order | each { |name|
    var body = $edit:small-word-abbr[$name]
    echo (styled $name green)(styled ' -> ' cyan)$body
  }
}
