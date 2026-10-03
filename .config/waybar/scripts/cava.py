#!/usr/bin/env python3
"""Sideways audio visualizer: cava raw output -> block glyphs (waybar rotates them)."""
import json, os, shutil, subprocess, sys

if not shutil.which("cava"):
    print(json.dumps({"text": "", "class": "missing"}), flush=True)
    sys.exit(0)

BLOCKS = "▁▂▃▄▅▆▇█"
conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cava.conf")
proc = subprocess.Popen(["cava", "-p", conf], stdout=subprocess.PIPE, text=True)
last = None
for line in proc.stdout:
    vals = [int(v) for v in line.strip().strip(";").split(";") if v]
    text = "".join(BLOCKS[v] for v in vals)
    if text == last:
        continue
    last = text
    cls = "idle" if not any(vals) else "playing"
    print(json.dumps({"text": text, "class": cls}), flush=True)
