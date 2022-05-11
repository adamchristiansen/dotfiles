use util

var config = [
  &before-text="\n"
  &before-style=[]

  &dir-prefix=' '
  &dir-suffix=''
  &dir-style=[blue bold]

  &duration-prefix=' '
  &duration-suffix=''
  &duration-style=[yellow bold]
  &duration-show=1000
  &duration-hide-millis=10_000

  &extra-text="\n"
  &extra-style=[]

  &git-branch-prefix=' '
  &git-branch-suffix=''
  &git-branch-style=[magenta bold]

  &jobs-text=' ●'
  &jobs-style=[cyan bold]

  &git-status-prefix=' ['
  &git-status-suffix=']'
  &git-status-style=[cyan bold]
  &git-status-order=[
    added deleted modified renamed
    untracked
    stashed
    unmerged
    ahead behind diverged
  ]
  &git-status-added='+'
  &git-status-ahead='↑'
  &git-status-behind='↓'
  &git-status-diverged='⇵'
  &git-status-deleted='-'
  &git-status-modified='!'
  &git-status-renamed='»'
  &git-status-stashed='#'
  &git-status-unmerged='='
  &git-status-untracked='?'

  &ssh-text=' ▲'
  &ssh-style=[cyan bold]

  &vert-bottom-ok-text='│ '
  &vert-bottom-ok-style=[green bold]
  &vert-bottom-fail-text='│ '
  &vert-bottom-fail-style=[red bold]

  &vert-top-ok-text='│'
  &vert-top-ok-style=[green bold]
  &vert-top-fail-text='│'
  &vert-top-fail-style=[red bold]
]

# A colleciton of data from edit:after-command
var after-command = [
  &duration=0
  &ok=$true
]

set @edit:after-command = $@edit:after-command { |result|
  set after-command[duration] = $result[duration]
  set after-command[ok] = (eq $result[error] $nil)
}

fn single-style { |name|
  var text = $config[(put $name)-text]
  var style = $config[(put $name)-style]
  styled $text (all $style)
}

fn compound-style { |name text|
  var prefix = $config[(put $name)-prefix]
  var suffix = $config[(put $name)-suffix]
  var style = $config[(put $name)-style]
  styled $prefix$text$suffix (all $style)
}

fn prompt-before {
  single-style before
}

fn prompt-vert-top {
  if $after-command[ok] {
    single-style vert-top-ok
  } else {
    single-style vert-top-fail
  }
}

fn prompt-vert-bottom {
  if $after-command[ok] {
    single-style vert-bottom-ok
  } else {
    single-style vert-bottom-fail
  }
}

fn prompt-jobs {
  if (> $num-bg-jobs 0) {
    single-style jobs
  }
}

fn prompt-ssh {
  if (or (has-env SSH_CLIENT) (has-env SSH_CONNECTION) (has-env SSH_TTY)) {
    single-style ssh
  }
}

fn prompt-dir {
  use path
  use str

  var dir
  if ?(git status > /dev/null 2>&1) {
    var git-root = (git rev-parse --show-toplevel)
    var git-parent = (path:dir $git-root)
    set dir = (str:trim-left (str:trim-prefix $pwd $git-parent) '/')
  } else {
    set dir = (tilde-abbr $pwd)
  }
  compound-style dir $dir
}

fn git-info {
  use re
  use str

  var info = [
    &added=$false
    &ahead=$false
    &behind=$false
    &branch=$nil
    &deleted=$false
    &diverged=$nil
    &modified=$false
    &renamed=$false
    &stashed=$true
    &unmerged=$false
    &untracked=$false
  ]

  var status
  try {
    set info[branch] = (e:git rev-parse --abbrev-ref HEAD 2> /dev/null)
    set info[stashed] = (util:not-empty (git stash list 2> /dev/null | slurp))
    set @status = (e:git status --porcelain -b 2> /dev/null)
  } catch {
    # This is not a git repository
    return
  }

  # The first line is dropped because it contains branch information, not file
  # information.
  all $status | drop 1 | each { |line|
    var s = (str:split '' $line | take 2 | str:join '')
    if (str:contains $s 'A') { set info[added] = $true }
    if (str:contains $s 'D') { set info[deleted] = $true }
    if (str:contains $s 'M') { set info[modified] =  $true }
    if (str:contains $s 'R') { set info[renamed] =  $true }
    if (str:contains $s 'U') { set info[unmerged] =  $true }
    if (str:contains $s '?') { set info[untracked] = $true }
  }

  # The first line of the status contains the branch divergence information.
  var first = (all $status | take 1)
  var ahead = (re:match '\[.*ahead.*\]' $first)
  var behind = (re:match '\[.*behind.*\]' $first)
  var diverged = (and $ahead $behind)
  set info[ahead] = (and $ahead (not $diverged))
  set info[behind] = (and $behind (not $diverged))
  set info[diverged] = $diverged

  put $info
}

fn prompt-git-branch {
  try {
    var info = (git-info | one)
    compound-style git-branch $info[branch]
  } catch {
    return
  }
}

fn prompt-git-status {
  var info
  try {
    set info = (git-info | one)
  } catch {
    # Not a git repository
    return
  }

  var status = ''
  all $config[git-status-order] | each { |item|
    if $info[$item] {
      set status = $status$config[git-status-$item]
    }
  }
  if (util:not-empty $status) {
    compound-style git-status $status
  }
}

fn prompt-duration {
  # The total duration in milliseconds of the previous command
  var millis = (util:int (* 1000 $after-command[duration]))
  if (< $millis $config[duration-show]) {
    return
  }
  var show-millis = (< $millis $config[duration-hide-millis])
  var duration = (util:humanize-duration &show-millis=$show-millis $millis)
  compound-style duration $duration
}

fn prompt-extra {
  single-style extra
}

set edit:prompt = {
  prompt-before
  prompt-vert-top
  prompt-ssh
  prompt-jobs
  prompt-dir
  prompt-git-branch
  prompt-git-status
  prompt-duration
  prompt-extra
  prompt-vert-bottom
}

# Disable right prompt
set edit:rprompt = { }
