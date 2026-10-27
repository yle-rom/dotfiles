#!/usr/bin/env bash
# Emergency mode: red palette + pulsing border on all 4 bars when battery is critical and discharging.
# The banner itself is drawn by dayclock.py top (same rule, same test flag); this module only watches.
#   emergency.sh        -> watcher (run by waybar every few seconds)
#   emergency.sh test   -> toggle a fake emergency so you can see it without draining the battery
DIR="$(cd "$(dirname "$0")" && pwd)"      # scripts/ (emergency-on/off.css)
WAYBAR="$(dirname "$DIR")"                # waybar root (style.css, emergency.css)
CSS="$WAYBAR/emergency.css"
FLAG="${XDG_RUNTIME_DIR:-/tmp}/waybar-emergency-test"
CRITICAL=10

if [[ $1 == test ]]; then
  if [[ -e $FLAG ]]; then rm "$FLAG"; echo "emergency test OFF"; else touch "$FLAG"; echo "emergency test ON"; fi
  exit 0
fi

bat=$(echo /sys/class/power_supply/BAT*)
cap=$(<"$bat/capacity"); status=$(<"$bat/status")
if [[ -e $FLAG ]] || { (( cap <= CRITICAL )) && [[ $status == Discharging ]]; }; then
  want="$DIR/emergency-on.css"
else
  want="$DIR/emergency-off.css"
fi

# Swap palette only on change.
if ! cmp -s "$want" "$CSS"; then
  cp "$want" "$CSS"
  # each bar's reload_style_on_change watches only its own -s file (not imports): re-write every style*.css
  # to trigger a reload on all 4 bars (lighter than SIGUSR2, which restarts every module)
  for f in "$WAYBAR"/style*.css; do s=$(<"$f"); printf '%s\n' "$s" > "$f"; done
fi

if [[ $want == *on.css ]]; then
  echo '{"text":"","class":"emergency"}'          # no label: the top bar's clock shows the banner
else
  echo '{"text":"","class":"normal"}'
fi
