function psgrep --description="Search running processes"
  set -l args $argv
  for i in (seq 1 1 (count $args) 2> /dev/null)
    set -l a $args[$i]
    # Only modify the argument if it is not an option
    if [ (string sub -s 1 -l 1 -- $a) != - ]
      # The argument does not start with a "-", so wrap the first
      # character in [] to prevent it from showing up in the grep output
      set args[$i] "["(string sub -s 1 -l 1 -- $a)"]"(string sub -s 2 -- $a)
    end
  end
  ps aux | grep $args
end
