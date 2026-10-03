#!/usr/bin/env python3
"""24h ruler: one tick per 2 hours, labels every 6h, the current slot shows the exact time."""
import json
from datetime import datetime

now = datetime.now()
lines = []
for h in range(0, 24, 2):
    if h <= now.hour < h + 2:
        lines.append(f"<span size='9pt'><b>{now:%H:%M}</b></span>")
    elif h % 6 == 0:
        lines.append(f"<span size='6pt' alpha='70%'>{h:02d}</span>")
    else:
        lines.append(f"<span size='6pt' alpha='35%'>──</span>")
print(json.dumps({"text": "\n".join(lines), "tooltip": f"{now:%H:%M · %A %d %B}"}))
