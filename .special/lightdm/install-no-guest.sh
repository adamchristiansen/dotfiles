#!/usr/bin/env sh

d=/etc/lightdm/lightdm.conf.d
f=50-no-guest.conf

sudo install -D -m 644 -o root "$f" "$d/$f"
