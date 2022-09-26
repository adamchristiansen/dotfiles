#!/usr/bin/env sh

set -e

# Make sure the script executes in the directory of this file
cd "$(dirname "$(realpath "$0")")"

sudo install -m 755 -o root fstrim /etc/cron.weekly
