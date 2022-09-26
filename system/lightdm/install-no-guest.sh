#!/usr/bin/env sh

set -e

# Make sure the script executes in the directory of this file
cd "$(dirname "$(realpath "$0")")"

d=/etc/lightdm/lightdm.conf.d
f=50-no-guest.conf

sudo install -D -m 644 -o root "$f" "$d/$f"
