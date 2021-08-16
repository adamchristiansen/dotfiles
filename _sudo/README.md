# Sudo Lecture

This is used to add a custom `sudo` lecture. Run

```sh
sh install-lecture.sh
```
to install it, then use `visudo` and set the following options

```
Defaults lecture = "always"
Defaults lecture_file = "/etc/sudo.lecture"
```

The lecture is a modified version of https://redd.it/6lyvx1.
