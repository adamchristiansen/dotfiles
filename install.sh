#!/usr/bin/env sh

# A quick script to install the latest version of chezmoi if it is not
# found in the PATH.
#
# When -f is given as the only argument to this script, a download of the
# latest version is forced. This can be used as a basic way of getting updates.

install_dir="$HOME/.local/bin"

if [ "$1" != "-f" ] && command -v chezmoi > /dev/null; then
  echo "Already installed"
  exit 0
fi

if command -v curl > /dev/null; then
  sh -c "$(curl -fsSL 'https://git.io/chezmoi')" -- -b "$install_dir"
elif command -v wget > /dev/null; then
  sh -c "$(wget -qO- 'https://git.io/chezmoi')" -- -b "$install_dir"
else
  echo "Requires curl or wget" >&2
  exit 1
fi
