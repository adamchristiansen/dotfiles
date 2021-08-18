#!/usr/bin/env sh

# Tells all running processes to reload their config files.

# Send SIGUSR1 to any processes with the name $1.
send_sigusr1() {
    killall -SIGUSR1 "$1" > /dev/null 2>&1
}

# If at least one instance of the program in $1 is running, then execute the
# command in $2.
when_running() {
    # Change the format of the command "name" to "[n]ame". Adding these
    # brackets prevents grep from reporting itself in the process list
    h=$(echo "$1" | awk '{print substr($1,0,1)}')
    t=$(echo "$1" | awk '{print substr($1,2)}')
    query="[$h]$t"

    if [ ! -z "$(ps aux | grep "$query")" ]; then
        $2 > /dev/null 2>&1 &
    fi
}

when_running berry "$XDG_CONFIG_HOME/berry/autostart 1"
when_running bspwm "$XDG_CONFIG_HOME/bspwm/bspwmrc 1"
send_sigusr1 nvim
send_sigusr1 picom
when_running qutebrowser "qutebrowser --target=tab-silent :config-source"
send_sigusr1 sxhkd
when_running tmux "tmux source-file ~/.config/tmux/tmux.conf"

# This script always exits successfully
exit 0
