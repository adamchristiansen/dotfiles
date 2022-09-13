# Home Configuration

These are user configurations that are automatically installed in the home
directory.



## Color Themes

If a `chezmoi` template needs access to colors, then include

```
{{- $color := include ".gen/color.json" | mustFromJson -}}
```

at the top of the template. Colors can then be accessed through the `$color`
variable, such as

```
{{ $color.base0a.hex.rgb }}
```

See the [color README](dot_config/exact_color/README.md) for more information
on using colors.
