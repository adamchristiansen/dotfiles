use re
use util

fn new { |name body|
  set edit:small-word-abbr[$name] = $body
}

# Parse abbreviations in a file and add them. The file may contain the
# following:
#
# - Lines that are ignored:
#   - Lines that consist of only whitespace
#   - Lines where the first non-whitespace character is #
# - Lines containing an alias of the form:
#   - alias gs='git status'
#   - alias gs="git status"
#   - alias g=git # A single 'word' with no spaces
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
    new $name $body
  }
}

fn list {
  keys $edit:abbr | order | each { |name|
    var body = $edit:abbr[$name]
    echo (styled $name green bold)(styled ' -> ' cyan)$body
  }
}
