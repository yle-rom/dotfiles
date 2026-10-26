# waybar

NERV bars, two of them, both started by hypr `autostart.lua`:

| bar | files | holds | toggle |
|---|---|---|---|
| left | `config` + `style.css` | power, battery, volume, day clock, weather/moon, sync, cava, ws 1-4 | `mainMod+B` |
| right | `config-right` + `style-right.css` | power, cpu, net rain, pet, ws 5-8 | `mainMod+N` |

`style-right.css` imports `style.css`, so colors, fonts and emergency mode carry over.
`mainMod+I` (`~/.local/bin/dashboard-toggle`) hides both while the dashboard is open.
Both bars have `reload_style_on_change`: saving a css reloads it live.

## colors
`style.css` imports `colors-active.css`, a symlink `rice` flips between:
- `~/.cache/wal/colors-waybar.css` (pywal, from `~/.config/wal/templates/`)
- `colors-custom.css` (fixed palette)

Wallpaper picker (`~/.config/quickshell/hyprquickpaper/commands.sh`) re-applies colors by
re-writing `style.css` + `style-right.css` in place (triggers `reload_style_on_change`).

## emergency
`emergency.sh` (polled) copies `scripts/emergency-{on,off}.css` → `emergency.css`
(imported by style.css), then re-writes style.css to force a reload.
Battery ≤10% + discharging = red. Test: `scripts/emergency.sh test` (toggle).

## scripts/
| file | module / use |
|---|---|
| workspaces.py N | workspace button N (1-8), Eva kanji 零初弐参使魂槍月 + window dots |
| dayclock.py bar\|time | day meter (10 cells, 2.4 h each) + HH/MM; calendar tooltip from blockclock.py |
| weather.py --moon (+moon.py) | weather + moon phase, pinned to Ioannina; click → wttr.in |
| sysmon.py cpu\|net | cpu load waterfall + temp; net braille rain |
| toys.py sync\|pet [H]\|rain | typing "sync ratio"; braille pet (H = track height, right bar uses 92); katakana rain (unused) |
| cava.py (+cava.conf) | audio visualizer |
| emergency.sh (+on/off css) | see above |
| calpopup.py | calendar popup on clock click |
| blockclock.py | old block clock (not in a bar; kept for its calendar tooltip) |
| menu-theme.sh | shared rofi theme, sourced by `magitl`/`powermenu` (~/.local/src/scripts) |

Clicks also call `~/.local/bin/magitl` (power profile), `powermenu`, `pavucontrol`.
Old bars/experiments/backups: `~/.config/vault/waybar/`.

## how the animated modules work
All are long-running scripts printing one JSON line (`text`/`class`/`tooltip`) per frame;
waybar redraws on every line. Graphics are text: braille (U+2800, each char = 2x4 dots)
and block characters, so a "pixel grid" is just a list of rows turned into characters.

**sync (typing speed)** `toys.py sync`
- Reading keys needs the `input` group (= any process could keylog). Instead: the built-in
  keyboard's interrupt counter, IRQ 1 `i8042` in `/proc/interrupts`, readable by anyone.
- Every key fires ~2.1 interrupts (press + release; measured: 574 for a 274-char test).
  Over a 3 s window: `chars = Δirq / 2.1`, `wpm = chars / 5 per minute`, divided by how long
  you've actually been typing (min 1 s) so it reads true speed after ~1 s.
- Shown value eases toward the target (rises fast, falls faster); sync % = wpm 1:1.
  ≥130% blinks red. USB keyboards aren't counted (different IRQ).

**pet** `toys.py pet 92`
- 8x6 dot sprites (open / blink / step / sleep) drawn into an 8 x H dot grid, converted to braille.
- Walks up and down the track, pauses and turns at random, blinks every ~4 s.
- Sleeps (dim + z Z) 00-07h or after 2 min with no keyboard interrupts; sweats + red at CPU ≥80°C.
- Has its own copy of the sync meter: 2x speed from 60%, 3x from 100%, no dawdling.

**net rain** `sysmon.py net`
- Bytes from `/proc/net/dev` (all interfaces except lo/virbr/docker/veth/br-), delta per frame.
- An 8 x 72 dot grid: download dots spawn at the top of the left half and fall one row per
  frame; upload dots spawn at the bottom of the right half and rise.
- Spawn chance per column = rate on a log scale (~1 KB/s drizzle → ~10 MB/s pours).
  No numbers on the bar; the tooltip has them but rarely shows (see gotchas).

**cpu** `sysmon.py cpu`: load from `/proc/stat` deltas, one row per frame, newest on top,
older rows fade (alpha); rows grow from the center using left- and right-aligned eighth
blocks (Adwaita Mono has the right-aligned ones); sqrt scale so idle load stays visible.
Temp from hwmon `coretemp` (found by name; hwmon numbers change per boot).

## gotchas
- **No `SIGUSR2`** to waybar: the left bar aborts on reload (GLib `object_id != 0`).
  pywal sends one too, so the wallpaper picker runs `wal -e`. Restart a bar by killing it
  (`pkill -fx waybar` = left, `pkill -f '^waybar -c .*config-right'` = right) and starting it.
- **Tooltips**: a module whose output keeps changing blocks hover tooltips for its whole bar.
  Print only on change; animated/live modules get `"tooltip": false` (sync) or no tooltip use.
