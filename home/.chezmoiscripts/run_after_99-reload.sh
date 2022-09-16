#!/usr/bin/env sh

# Tells all running processes to reload their config files.

set -e

# Send SIGUSR1 to any processes with the name $1.
send_sigusr1() {
  killall -SIGUSR1 "$1" > /dev/null 2>&1
}

# If at least one instance of the program in $1 is running, then execute the
# command in $2.
when_running() {
  if pgrep -x "$1" > /dev/null; then
    $2 > /dev/null 2>&1 &
  fi
}

when_running bspwm "$XDG_CONFIG_HOME/bspwm/bspwmrc"
send_sigusr1 picom
when_running qutebrowser "qutebrowser --target=tab-silent :config-source"
send_sigusr1 sxhkd
when_running tmux "tmux source-file $XDG_CONFIG_HOME/tmux/tmux.conf"

# This script always exits successfully
exit 0
