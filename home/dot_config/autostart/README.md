# Autostart Environment Variables

To run autostart applications with all environment variables loaded, make the
file a template and use:

```
Exec={{ .chezmoi.homeDir }}/.local/bin-dotfiles/bashful app_start_cmd arg1 arg2 ...
```

To run the `app_start_cmd` with the specified arguments.
