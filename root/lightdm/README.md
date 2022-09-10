# LightDM

### Disable Guest Session

Put the file `50-no-guest.conf` in `/etc/lightdm/lightdm.conf.d/` to disable the
guest session. Delete this file to re-enable it.

The `install-no-guest.sh` script can be executed from this directory to install
the file.
