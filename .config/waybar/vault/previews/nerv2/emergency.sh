#!/usr/bin/env bash
# Emergency mode: red palette + pulsing border when battery is critical and discharging.
#   emergency.sh        -> watcher (run by waybar every few seconds)
#   emergency.sh test   -> toggle a fake emergency so you can see it without draining the battery
DIR="$(cd "$(dirname "$0")" && pwd)"
CSS="$DIR/emergency.css"
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
  # reload_style_on_change watches style.css itself, so re-write it to trigger a style reload
  # (no SIGUSR2: that restarts everything and crashes a second waybar instance on 0.15)
  s=$(<"$DIR/style.css"); printf '%s\n' "$s" > "$DIR/style.css"
fi

if [[ $want == *on.css ]]; then
  printf '{"text":"非常\\n事態","class":"emergency","tooltip":"EMERGENCY · battery %s%%"}\n' "$cap"
else
  echo '{"text":"","class":"normal"}'
fi
