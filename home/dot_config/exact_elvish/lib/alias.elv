use re
use util

var aliases = [&]

fn new { |name body|
  var fn~ = { }
  eval 'set fn~ = { |@args| '$body' $@args  }'
  edit:add-var $name'~' $fn~
  set aliases[$name] = [&fn=$fn~ &body=$body]
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
      fail 'Alias syntax error: '$line
    }
    var name = $match[0][groups][1][text]
    var body = $match[0][groups][2][text]
    # Expand $(...) -> (...)
    set body = (re:replace '\$\(' '(' $body)
    new $name $body
  }
}

fn list {
  keys $aliases | order | each { |name|
    var body = $aliases[$name][body]
    echo (styled $name green)(styled ' -> ' cyan)$body
  }
}
