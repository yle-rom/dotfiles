#!/usr/bin/env bash
# The 4-bar frame. Usage: frame.sh start|stop|toggle
# Used by hypr autostart, mainMod+B and dashboard-toggle, so the start order lives in one place.
W=~/.config/waybar

start() {
  pgrep -x waybar >/dev/null && return
  # sides first: layer-shell exclusive zones stack in start order, so the side bars run full height
  # and own the corners; top/bottom then fit between them
  for b in left right; do setsid -f waybar -c "$W/config-$b" -s "$W/style-$b.css" >/dev/null 2>&1; done
  # wait until both side bars are mapped (measured ~0.13 s), at most 3 s
  for _ in {1..150}; do
    (( $(hyprctl layers | command grep -c "namespace: waybar") >= 2 )) && break
    sleep 0.02
  done
  for b in top bottom; do setsid -f waybar -c "$W/config-$b" -s "$W/style-$b.css" >/dev/null 2>&1; done
}

stop() { pkill -x waybar; }                  # process name: every waybar is part of the frame

case $1 in
  start) start ;;
  stop) stop ;;
  toggle) if pgrep -x waybar >/dev/null; then stop; else start; fi ;;
  *) echo "usage: frame.sh start|stop|toggle" >&2; exit 1 ;;
esac
