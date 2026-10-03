#!/usr/bin/env python3
"""Vertical week strip: month label + this week's dates, today highlighted (pywal colors)."""
import json, os
from datetime import date, timedelta

c = open(os.path.expanduser("~/.cache/wal/colors")).read().split()
bg, fg = c[0], c[3]
today = date.today()
monday = today - timedelta(days=today.weekday())
lines = [f"<span size='8pt' alpha='60%'>{today:%b}</span>".replace(f'{today:%b}', f'{today:%b}'.upper())]
for i in range(7):
    d = monday + timedelta(days=i)
    if d == today:
        lines.append(f"<span background='{fg}' foreground='{bg}'><b> {d:%d} </b></span>")
    else:
        alpha = "30%" if i >= 5 else "55%"
        lines.append(f"<span alpha='{alpha}'>{d:%d}</span>")
print(json.dumps({"text": "\n".join(lines), "tooltip": f"{today:%A %d %B %Y · week %V}"}))
