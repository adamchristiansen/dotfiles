#!/usr/bin/env sh

# Apply a new crontab.

set -e

if ! type crontab > /dev/null 2>&1; then
  exit
fi

export EDITOR="$HOME/.config/crontab/crontab-apply"
export VISUAL="$EDITOR"
crontab -e > /dev/null 2>&1
