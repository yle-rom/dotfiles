#!/usr/bin/env python3
"""Clock, two styles (first argument):
  cjk    big heavy Noto Sans CJK digits, NERV title-card style,
         a grid of squares (10 rows of 6) under them that fills one dot per second; updates every second
  block  (default) drawn with block characters: a 3x5 pixel font, two pixel rows per text row (▀ ▄ █),
         with the same seconds grid under it
Tooltip: this month's calendar in the bar's colors (colors-active.css)."""
import calendar, json, os, re, sys, time
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


def block(now):
    gap = lambda px: f"<span size='{px * 1024 * 3 // 4}'> </span>"  # empty line of a given height (px -> 1/1024 pt)
    digits = render(f"{now:%H}") + [gap(3)] + render(f"{now:%M}") + [gap(10)]
    return "<span line_height='0.7'>" + "\n".join(digits) + "</span>\n" + seconds(now)  # rows touch: solid digits


def cjk(now):  # size set here, not in style.css, so the 7px block pixels stay as they are
    font = "font_family='Noto Sans CJK JP'"
    return (f"<span {font} size='20pt' weight='heavy' line_height='0.85'>"
            f"{now:%H}\n{now:%M}</span>\n"
            f"{seconds(now)}")


def seconds(now):  # 10 rows x 6 square grid, one square per elapsed second; empty squares dimmed
    dots = ["■" if i < now.second else "<span alpha='20%'>■</span>" for i in range(60)]
    rows = ("".join(dots[r:r + 6]) for r in range(0, 60, 6))
    return "<span font_family='JetBrainsMono NFM' size='5pt' letter_spacing='1536' line_height='0.8'>" + "\n".join(rows) + "</span>"


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


style = sys.argv[1] if len(sys.argv) > 1 else "block"
draw, tick = {"cjk": (cjk, 1), "block": (block, 1)}[style]  # tick: seconds between redraws
while True:
    now = datetime.now()
    print(json.dumps({"text": draw(now), "tooltip": month_tooltip(now)}), flush=True)
    time.sleep(tick - time.time() % tick + 0.05)  # wake just after the next second / minute boundary
