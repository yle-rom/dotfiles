#!/usr/bin/env python3
"""Day meter clock, styled like the battery/volume meters.
  dayclock.py bar   -> how much of the day (00:00-24:00) has passed, as a bar (waybar rotates it)
  dayclock.py time  -> HH over MM
Tooltip: this month's calendar (from blockclock.py)."""
import json, sys, time
from datetime import datetime
from blockclock import month_tooltip



def bar(frac, cells=10):  # same 10 whole cells as the battery bar, no partial cell (one cell = 2.4 h)
    full = round(frac * cells)
    return "█" * full + "░" * (cells - full)


mode = sys.argv[1] if len(sys.argv) > 1 else "time"
last = None
while True:
    t = time.time()
    now = datetime.fromtimestamp(t)
    if mode == "bar":
        text = bar((now.hour + now.minute / 60) / 24)
    else:
        text = f"<span line_height='0.85'>{now:%H}\n{now:%M}</span>"
    out = json.dumps({"text": text, "tooltip": month_tooltip(now)})
    if out != last:                           # print only on change: constant re-sends keep the tooltip from showing
        print(out, flush=True)
        last = out
    time.sleep(1 - t % 1 + 0.02)              # wake just after each second
