#!/usr/bin/env sh

set -e

# Make sure the script executes in the directory of this file
cd "$(dirname "$(realpath "$0")")"

echo "$(cat sudo.lecture)" | sudo tee /etc/sudo.lecture > /dev/null
