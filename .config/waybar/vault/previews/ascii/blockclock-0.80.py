#!/usr/bin/env python3
"""Time drawn with block characters: a 3x5 pixel font, two pixel rows per text row (▀ ▄ █)."""
import json, sys, time
from datetime import datetime

FONT = {  # 3 wide x 5 tall
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", "###", "..#", "###"],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
    "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", "..#", "..#", "..#"],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
}
HALF = {(True, True): "█", (True, False): "▀", (False, True): "▄", (False, False): " "}


def render(num):
    rows = [" ".join(FONT[d][r] for d in num) for r in range(5)] + ["." * 7]
    out = []
    for r in range(0, 6, 2):
        out.append("".join(HALF[(a == "#", b == "#")] for a, b in zip(rows[r], rows[r + 1])))
    return out


while True:
    now = datetime.now()
    lines = render(f"{now:%H}") + [""] + render(f"{now:%M}")
    text = "<span line_height='0.80'>" + "\n".join(lines) + "</span>"
    print(json.dumps({"text": text, "tooltip": f"{now:%H:%M}"}), flush=True)
    time.sleep(60 - datetime.now().second + 0.2)
