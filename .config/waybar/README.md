# waybar

NERV frame: four bars around the screen, started by `scripts/frame.sh` (hypr `autostart.lua`).

```
┌─ top ─────────────────────────────────────────────────────────────────────────┐
│ EVA-01 SYNC 0.0%        MON 26 OCT ██████░░░░ 20:49     ♥ 63  ◉ 80  🔥 57°  ◯ 11° CLEAR │
left                                                                          right
power · kana rain · ws 1-4                                    power · net stream · ws 5-8
│ 󰒮 󰏤 󰒭  artist — title ████░░░░   pet walks here …            ▂▃▅▇▅▃▂ cava │
└─ bottom ──────────────────────────────────────────────────────────────────────┘
```

| bar | files | holds |
|---|---|---|
| left | `config-left` + `style-left.css` | power, katakana rain (`toys.py rain 56`), emergency watcher (no label), ws 1-4 |
| right | `config-right` + `style-right.css` | power, net stream (`sysmon.py net 77`), ws 5-8 |
| top | `config-top` + `style-top.css` | `EVA-01` (static), sync · date + day meter + time · battery, volume, cpu temp, weather + moon |
| bottom | `config-bottom` + `style-bottom.css` | prev/play/next, track + progress, pet · cava |

`style.css` is the shared base (colors, fonts, workspace/power styles, emergency import); every
`style-*.css` imports it and adds that bar's own line and modules.
All four bars use ShureTechMono Nerd Font Mono (one `window#waybar.<pos> *` rule each, CJK fallback
for kanji); braille (pet) and blocks (cava) stay JetBrains, kana rain stays Noto CJK.

## frame.sh
`frame.sh start|stop|toggle`. **Start order matters**: layer-shell exclusive zones stack in start
order, so the sides start first (full height, they own the corners) and top/bottom start as soon
as `hyprctl layers` shows both sides mapped (~0.13 s, capped at 3 s), fitting between them.
All 4 are up in ~0.3 s. Stop = `pkill -x waybar` (every waybar is part of the frame).
Callers: hypr `autostart.lua` (start), `mainMod+B` (toggle all 4), `dashboard-toggle` (stop on
open, start on close).

## layout numbers (eDP-2, 2560x1600 @1.6 = 1600x1000 logical)
- Each bar is 35px; with `gaps_out = 20` a tiled window is 1488x888 logical.
- Inner lines: top/bottom use a 1px border; the sides draw theirs as a background layer with
  34px `@bg` covers at both ends (GTK3 CSS can't draw a partial border, no `calc()`), so the
  corners join as an L. Relies on `@bg` being opaque.
- **20px edge padding = `gaps_out`** on `EVA-01`, the weather and cava: they line up with a tiled
  window's edges. Change `gaps_out` → change those paddings.
- Top-bar baseline: every label carries a zero-width char in JetBrainsMono NFP 13pt (the moon's
  font/size), so all lines get the same height and one baseline.
- Rain (56 rows) and net stream (77 rows) are both 1321px tall (rows differ in height).

## colors
`style.css` imports `colors-active.css`, a symlink `rice` flips between:
- `~/.cache/wal/colors-waybar.css` (pywal, from `~/.config/wal/templates/`)
- `colors-custom.css` (fixed palette)

Wallpaper picker (`~/.config/quickshell/hyprquickpaper/commands.sh`) re-applies colors by
re-writing every `style*.css` in place (triggers `reload_style_on_change`).

## emergency
Battery ≤10% + discharging → every bar turns red and the top clock becomes a blinking
`非常事態  EMERGENCY  非常事態` banner (same 29-cell width as the date line).
- `emergency.sh` (polled by the left bar, prints no text) copies `scripts/emergency-{on,off}.css`
  → `emergency.css` (imported by style.css), then re-writes every `style*.css` so all 4 bars reload.
- `dayclock.py top` checks the same rule and the same test flag and swaps in the banner.
- Test: `scripts/emergency.sh test` (toggle).

## scripts/
| file | module / use |
|---|---|
| frame.sh | start/stop/toggle the 4 bars (see above) |
| workspaces.py N | workspace button N (1-8), Eva kanji 零初弐参使魂槍月 + window dots |
| dayclock.py top\|bar\|time | `top`: date + day meter (10 cells, 2.4 h each) + HH:MM, emergency banner; calendar tooltip from blockclock.py |
| weather.py --top (+moon.py) | moon glyph, temp, condition; pinned to Ioannina; click → wttr.in |
| sysmon.py cpu-top\|net [rows]\|cpu | `cpu-top`: fire icon + temp (load in tooltip); `net`: braille rain; `cpu`: old waterfall (unused) |
| toys.py sync-top\|rain [rows]\|sync\|pet | `sync-top`: one-line sync ratio; `rain`: katakana rain; `sync`/`pet`: old vertical versions (unused) |
| media.py ctl prev\|play\|next / track / pet | media buttons (playerctl), title + progress, bottom-bar pet |
| cava.py (+cava.conf) | audio visualizer, 32 bars, block glyphs |
| emergency.sh (+on/off css) | see above |
| calpopup.py | calendar popup on clock click |
| blockclock.py | old block clock (not in a bar; kept for its calendar tooltip) |
| menu-theme.sh | shared rofi theme, sourced by `magitl`/`powermenu` (~/.local/src/scripts) |

Clicks also call `~/.local/bin/magitl` (battery: power profile), `powermenu`, `pavucontrol`, `nvtop`.
Old bars/experiments/backups: `~/.config/vault/waybar/` (pre-frame setup: `pre-frame-2026-10-26/`).

## how the animated modules work
All are long-running scripts printing one JSON line (`text`/`class`/`tooltip`) per frame;
waybar redraws on every line. Graphics are text: braille (U+2800, each char = 2x4 dots)
and block characters, so a "pixel grid" is just a list of rows turned into characters.

**sync (typing speed)** `toys.py sync-top`
- Reading keys needs the `input` group (= any process could keylog). Instead: the built-in
  keyboard's interrupt counter, IRQ 1 `i8042` in `/proc/interrupts`, readable by anyone.
- Every key fires ~2.1 interrupts (press + release; measured: 574 for a 274-char test).
  Over a 3 s window: `chars = Δirq / 2.1`, `wpm = chars / 5 per minute`, divided by how long
  you've actually been typing (min 1 s) so it reads true speed after ~1 s.
- Shown value eases toward the target (rises fast, falls faster); sync % = wpm 1:1.
  ≥130% blinks red. USB keyboards aren't counted (different IRQ). Number is right-padded
  so the bar doesn't shift.

**pet** `media.py pet` (sprites, typing meter and helpers imported from toys.py)
- 8x6 dot sprites (open / blink / step / sleep) on an 8-dot-tall strip = 2 braille lines,
  walking left/right, pausing and turning at random, blinking every ~4 s.
- Track width = `AVAIL` (926px, measured: title start x=116 → 12px before cava x=1066) minus
  what the title + progress bar use (6px cells, CJK = 2), so it always stops just before cava.
  **Re-measure `AVAIL`** if the buttons, cava's bar count or cava's padding change.
- Must be JetBrains braille at `line_height 1.0`: at 0.75 the two lines overlap one dot row and
  fill in the eyes. `margin-top: -8px` re-centers it.
- Sleeps 00-07h or after 2 min with no keyboard interrupts (a z blinks beside it). Sweat drop at
  CPU ≥80°C. 2x speed from 60% sync, 3x from 100%.

**net rain** `sysmon.py net 77`
- Bytes from `/proc/net/dev` (all interfaces except lo/virbr/docker/veth/br-), delta per frame.
- An 8 x (rows×4) dot grid: download dots spawn at the top of the left half and fall one row
  per frame; upload dots spawn at the bottom of the right half and rise.
- Spawn chance per column = rate on a log scale (~1 KB/s drizzle → ~10 MB/s pours).
  No numbers on the bar; the tooltip has them but rarely shows (see gotchas).

**kana rain** `toys.py rain 56`: 4 columns of half-width katakana, bright head, fading trail,
random speed; glyphs mutate. Decorative (a CPU-driven version was tried: load sat mostly on
the same cores, so one column did all the falling).

**cpu** `sysmon.py cpu-top`: temp from hwmon `coretemp` (found by name; hwmon numbers change per
boot), load from `/proc/stat` deltas into the tooltip; prints only on change. Yellow ≥70°,
pulsing red ≥85°, blinking red ≥95°.

## gotchas
- **No `SIGUSR2`** to waybar: the left bar aborts on reload (GLib `object_id != 0`).
  pywal sends one too, so the wallpaper picker runs `wal -e`. Restart with `frame.sh stop` + `start`.
- **`reload_style_on_change` watches only the bar's own `-s` file**, not its imports. Anything that
  changes shared CSS (emergency, colors) must re-write every `style*.css`. Each config needs the key.
- **Tooltips**: a module whose output keeps changing blocks hover tooltips for its whole bar.
  Print only on change; animated/live modules get `"tooltip": false` or no tooltip use.
- `pkill -f <pattern>` also matches the shell running it if the pattern appears in its own
  command line: anchor with `^waybar`.
