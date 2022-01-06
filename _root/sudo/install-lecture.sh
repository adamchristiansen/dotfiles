#!/usr/bin/env sh

echo "$(cat sudo.lecture)" | sudo tee /etc/sudo.lecture > /dev/null
