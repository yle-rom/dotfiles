#!/usr/bin/env python3
"""Clock drawn with block characters: a 3x5 pixel font, two pixel rows per text row (▀ ▄ █).
Tooltip: this month's calendar in the bar's colors (colors-active.css)."""
import calendar, json, os, re, time
from datetime import datetime

FONT = {  # 3 wide x 5 tall
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", "###", "..#", "###"],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
    "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", "..#", "..#", "..#"],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
}
HALF = {(True, True): "█", (True, False): "▀", (False, True): "▄", (False, False): " "}
COLORS = os.path.expanduser("~/.config/waybar/colors-active.css")


def render(num):
    rows = [" ".join(FONT[d][r] for d in num) for r in range(5)] + ["." * 7]
    return ["".join(HALF[(a == "#", b == "#")] for a, b in zip(rows[r], rows[r + 1])) for r in range(0, 6, 2)]


def color(name, default):
    try:
        m = re.search(rf"@define-color\s+{name}\s+(#[0-9a-fA-F]{{6}})", open(COLORS).read())
        return m.group(1) if m else default
    except OSError:
        return default


def month_tooltip(now):
    fg, bg = color("fg", "#5aaa53"), color("bg", "#0f1e0d")
    rows = [f"<b>{now:%B %Y}</b>".replace(f"{now:%B %Y}", f"{now:%B %Y}".upper()).center(27), "<span alpha='60%'>Mo Tu We Th Fr Sa Su</span>"]
    for week in calendar.Calendar(calendar.MONDAY).monthdayscalendar(now.year, now.month):
        cells = []
        for d in week:
            cell = f"{d:2d}" if d else "  "
            if d == now.day:
                cell = f"<span background='{fg}' foreground='{bg}'><b>{cell}</b></span>"
            cells.append(cell)
        rows.append(" ".join(cells))
    return "<tt>" + "\n".join(rows) + f"</tt>\n\n{now:%A %d %B · week %V}"


while True:
    now = datetime.now()
    digits = render(f"{now:%H}") + [""] + render(f"{now:%M}")
    text = "<span line_height='0.7'>" + "\n".join(digits) + "</span>"  # rows touch: solid digits
    print(json.dumps({"text": text, "tooltip": month_tooltip(now)}), flush=True)
    time.sleep(60 - datetime.now().second + 0.2)
