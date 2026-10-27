#!/usr/bin/env python3
"""Day meter clock, styled like the battery/volume meters.
  dayclock.py bar   -> how much of the day (00:00-24:00) has passed, as a bar (waybar rotates it)
  dayclock.py time  -> HH over MM
  dayclock.py top   -> "MON 26 OCT  ████░░  20:49" (top bar); an emergency banner while emergency.sh would fire
Tooltip: this month's calendar (from blockclock.py)."""
import json, sys, time
from datetime import datetime
from blockclock import month_tooltip



def bar(frac, cells=10):  # same 10 whole cells as the battery bar, no partial cell (one cell = 2.4 h)
    full = round(frac * cells)
    return "█" * full + "░" * (cells - full)


mode = sys.argv[1] if len(sys.argv) > 1 else "time"


def emergency():  # same rule as emergency.sh: battery <= 10% and discharging, or its test flag
    import glob, os
    if os.path.exists(os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "waybar-emergency-test")):
        return True
    bat = glob.glob("/sys/class/power_supply/BAT*")[0]
    return int(open(f"{bat}/capacity").read()) <= 10 and open(f"{bat}/status").read().strip() == "Discharging"

last = None
while True:
    t = time.time()
    now = datetime.fromtimestamp(t)
    if mode == "bar":
        text = bar((now.hour + now.minute / 60) / 24)
    elif mode == "top":   # horizontal: DATE  day meter  HH:MM
        text = (f"<span alpha='60%'>{now.strftime('%a %d %b').upper()}</span>  "
                + f"<span alpha='75%'>{bar((now.hour + now.minute / 60) / 24)}</span>  {now:%H:%M}")
    else:
        text = f"<span line_height='0.85'>{now:%H}\n{now:%M}</span>"
    cls = ""
    if mode == "top" and emergency():
        text, cls = "非常事態  EMERGENCY  非常事態", "emergency"       # 29 cells, like the date line it covers
    out = json.dumps({"text": text, "class": cls, "tooltip": month_tooltip(now)})
    if out != last:                           # print only on change: constant re-sends keep the tooltip from showing
        print(out, flush=True)
        last = out
    time.sleep(1 - t % 1 + 0.02)              # wake just after each second
