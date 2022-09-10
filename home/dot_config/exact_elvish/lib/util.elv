use math
use str

# Test if a path exists.
fn path-exists { |path|
  try {
    e:test -e $path
    put $true
  } catch _ {
    put $false
  }
}

# Test if a path exists and is a file.
fn file-exists { |path|
  try {
    e:test -f $path
    put $true
  } catch _ {
    put $false
  }
}

# Test if a process with a pid is running under the current user.
fn is-user-process { |pid|
  or (e:ps -u $E:USER | each { |line|
    ==s $pid [(str:split " " $line)][0]
  })
}

# Check if a container is empty.
fn empty { |value|
  == (count $value) 0
}

# Check if a container is not empty.
fn not-empty { |value|
  not (empty $value)
}

# Reverse a list.
fn reverse { |list|
  order &reverse=$true &less-than={|_ _| put $true } $list
}

# Find an enviroment variable. This first searches the supplied map to see if
# the name is in the map. If not in the map it searches environment variables
# under the `$E:` prefix. If nothing is found, then an empty string is
# returned.
fn find-env { |name &vs=[&]|
  if (has-key $vs $name) {
    put $vs[$name]
  } elif (has-env $name) {
    get-env $name
  } else {
    put ''
  }
}

# Coerce a number into an integer.
fn int { |n|
  put (printf "%.0f" $n)
}

# Division which returns an integer.
fn div { |n d| int (math:floor (/ $n $d)) }

# Modulo which returns an integer.
fn mod { |n d| int (% $n $d) }

# Turn a duration in milliseconds into a human readable format. If
# `show-millis` is set to `$false`, the milliseconds are not included and
# seconds are rounded appropriately.
fn humanize-duration { |&show-millis=$true millis|
  # Find the components of the duration
  var t = $millis
  var ms = (mod $t 1000)
  set t = (div $t 1000) # Time in seconds
  var s = (mod $t 60)
  set t = (div $t 60) # Time in minutes
  var m = (mod $t 60)
  set t = (div $t 60) # Time in hours
  var h = (mod $t 24)
  set t = (div $t 24) # Time in days
  var d = $t

  # Build the duration string
  var duration = ''
  if (!= $d 0) {
    set duration = $duration' '$d'd'
  }
  if (!= $h 0) {
    set duration = $duration' '$h'h'
  }
  if (!= $m 0) {
    set duration = $duration' '$m'm'
  }
  if (and (not $show-millis) (>= $ms 500)) {
    set s = (+ $s 1)
  }
  if (!= $s 0) {
    set duration = $duration' '$s's'
  }
  if (and $show-millis (!= $ms 0)) {
    set duration = $duration' '$ms'ms'
  }
  str:trim-space $duration
}
