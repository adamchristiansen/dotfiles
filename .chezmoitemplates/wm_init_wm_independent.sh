# Initialize the features common to all WMs.

# Start the keyring
if $startup; then
    if command -v gnome-keyring-daemon; then
        eval $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,keyring)
        export SSH_AUTH_SOCK
    fi
fi

# Set up the DPMS to be enabled with no timeout
xset +dpms
xset dpms 0 0 0

# Prevent the cursor from changing to an X when hovering over non-window
# space
xsetroot -cursor_name left_ptr &

# Launch the feature script passed in as the first argument.
if $startup; then
    launch_feature() {
        if [ -f "$1" ]; then
            "$1"
        else
            echo "Cannot start feature: launch script '$1' not found."
        fi
    }
    launch_feature "$XDG_CONFIG_HOME/dunst/launch"
    launch_feature "$XDG_CONFIG_HOME/mpd/launch"
    launch_feature "$XDG_CONFIG_HOME/picom/launch"
    launch_feature "$XDG_CONFIG_HOME/wallpaper/launch"
fi
