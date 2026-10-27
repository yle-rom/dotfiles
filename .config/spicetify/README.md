# spicetify

Theme `marketplace` (`Themes/marketplace/user.css`) gets every color from `--spice-*`
variables, so the palette lives only in `color.ini`. Two schemes in it:

- `pywal` — follows the wallpaper (default)
- `Spotify` — the original static brown/orange scheme

## How pywal drives it

```
wal  ->  ~/.config/wal/templates/colors-spicetify.ini   (template, tracked in dotfiles)
     ->  ~/.cache/wal/colors-spicetify.ini              (rendered on every wal run)
     <-  Themes/marketplace/color.ini                   (symlink to the rendered file)
```

`~/.config/quickshell/hyprquickpaper/commands.sh` runs `spicetify -q -n refresh` after `wal`.
`-n` = don't restart Spotify (a restart from that script kills Spotify), so **new colors
show on the next Spotify launch**.

Mapping (`[pywal]` section of the template):

| spice key | wal color |
|---|---|
| accent, banner, border-active, button, button-active | color3 (same as waybar/mako) |
| accent-active | color2 |
| main, main-elevated, sidebar, player, shadow | color0 |
| text / header | foreground / color15 |
| subtext, accent-inactive, border-inactive, button-disabled | color8 |
| highlight, card, selected-row, tab-active | color8 |
| notification / notification-error | color6 / color1 |

Player controls use `--spice-accent` (set in `user.css`, "player controls").

## Switching schemes

```sh
spicetify config color_scheme Spotify && spicetify apply   # original
spicetify config color_scheme pywal   && spicetify apply   # pywal
```

The `[Spotify]` section is kept inside the wal template, so it survives every wal run.
Edit colors in the template, never in `color.ini` (it is overwritten).

## Fresh setup / broken symlink

```sh
wal -R -n -e   # render templates from the current scheme
ln -sf ~/.cache/wal/colors-spicetify.ini ~/.config/spicetify/Themes/marketplace/color.ini
spicetify apply
```

## Backup

Pre-pywal state: `~/.config/vault/spicetify/` (config-xpui.ini + Themes/).
Restore: copy both back over these, `spicetify apply`.
