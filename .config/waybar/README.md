# waybar

NERV bar. Started by hypr `autostart.lua`. `config` = modules, `style.css` = look
(reloads on save).

## colors
`style.css` imports `colors-active.css`, a symlink `rice` flips between:
- `~/.cache/wal/colors-waybar.css` (pywal, from `~/.config/wal/templates/`)
- `colors-custom.css` (fixed palette)

## emergency
`emergency.sh` (polled) copies `scripts/emergency-{on,off}.css` → `emergency.css`
(imported by style.css), then re-writes style.css to force a reload.
Battery ≤10% + discharging = red. Test: `scripts/emergency.sh test` (toggle).

## scripts/
| file | module / use |
|---|---|
| workspaces.py N | custom workspace 1-4 buttons |
| cava.py (+cava.conf) | audio visualizer |
| emergency.sh (+on/off css) | see above |
| weather.py --moon (+moon.py) | weather + moon phase; click → wttr.in |
| blockclock.py | big block clock |
| calpopup.py | calendar popup on clock click |
| menu-theme.sh | shared rofi theme, sourced by `magitl`/`powermenu` (~/.local/src/scripts) |

Clicks also call `~/.local/bin/magitl` (power profile), `powermenu`, `pavucontrol`.
Old bars/experiments: `~/.config/vault/waybar/`.
