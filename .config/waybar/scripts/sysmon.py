#!/usr/bin/env python3
"""Animated system meters for the right bar. Usage: sysmon.py cpu|net. Streams JSON lines at FPS.
  cpu  load "waterfall" above a fire icon + temp (like the left bar's meters): one row per sample, newest on top, scrolling down
  net  a braille "data rain": dots fall for download, rise for upload, density = rate"""
import glob, json, math, random, socket, subprocess, sys, time
from collections import deque

FPS = 4
ROWS = 12                    # cpu waterfall height in text rows
NET_ROWS = 18                # net rain height in text rows
WIDTH = 4                    # cells per row (bar is 35px, 12px mono ~7px a cell)
EIGHTHS = " ▏▎▍▌▋▊▉█"                                  # left-aligned 0..8 eighths
EIGHTHS_R = " ▕\U0001FB87\U0001FB88▐\U0001FB89\U0001FB8A\U0001FB8B█"  # right-aligned (Legacy Computing block)


def emit(text, tooltip="", cls=""):
    print(json.dumps({"text": text, "tooltip": tooltip, "class": cls}), flush=True)


def hbar(frac):  # 0..1 -> WIDTH cells growing out from the middle, eighth-cell steps on each side
    frac = math.sqrt(max(0.0, min(1.0, frac)))   # sqrt: low loads stay visible (2% -> 14% of the width)
    half = WIDTH // 2
    n = round(frac * half * 8)                   # eighths filled on each side
    right = [EIGHTHS[max(0, min(8, n - 8 * i))] for i in range(half)]      # inner -> outer
    left = [EIGHTHS_R[max(0, min(8, n - 8 * i))] for i in range(half)]
    return "".join(reversed(left)) + "".join(right)


def waterfall(hist):  # newest row on top; older rows fade out
    rows = []
    for i, v in enumerate(hist):
        alpha = 100 - i * 70 // ROWS
        rows.append(f"<span alpha='{alpha}%'>{hbar(v)}</span>")
    # Adwaita Mono: JetBrains Mono lacks the right-aligned eighths, and both halves must share one font's metrics
    return "<span font_family='Adwaita Mono' line_height='0.75'>" + "\n".join(rows) + "</span>"


def level(t, warm, hot, crit):
    return "critical" if t >= crit else "hot" if t >= hot else "warm" if t >= warm else "cool"


# ---------- cpu ----------
def cpu_temp_path():  # hwmon numbers change between boots: find coretemp by name
    for h in glob.glob("/sys/class/hwmon/hwmon*"):
        if open(f"{h}/name").read().strip() == "coretemp":
            for lab in glob.glob(f"{h}/temp*_label"):
                if open(lab).read().startswith("Package"):
                    return lab.replace("_label", "_input")
    return None


def cpu_times():
    v = [int(x) for x in open("/proc/stat").readline().split()[1:]]
    idle = v[3] + v[4]                        # idle + iowait
    return sum(v) - idle, sum(v)


def cpu():
    tpath, hist = cpu_temp_path(), deque([0.0] * ROWS, maxlen=ROWS)
    busy0, total0 = cpu_times()
    while True:
        time.sleep(1 / FPS)
        busy, total = cpu_times()
        load = (busy - busy0) / max(1, total - total0)
        busy0, total0 = busy, total
        hist.appendleft(load)
        temp = int(open(tpath).read()) // 1000 if tpath else 0
        avg = sum(hist) / ROWS
        tip = f"CPU · {temp}°C package · load {avg:.0%} (last {ROWS / FPS:.1f}s)"
        emit(f"{waterfall(hist)}\n<span font_family='JetBrainsMono NFM' size='13.5pt'>\U000F0238</span>\n{temp}°", tip, level(temp, 70, 85, 95))


# ---------- net ----------
BRAILLE = [(0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08), (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80)]
COLS, DOTROWS = WIDTH * 2, NET_ROWS * 4          # dot grid (each braille cell = 2x4 dots)


def net_bytes():
    rx = tx = 0
    for line in open("/proc/net/dev").readlines()[2:]:
        name, data = line.split(":", 1)
        if name.strip() == "lo" or name.strip().startswith(("virbr", "docker", "veth", "br-")):
            continue
        f = data.split()
        rx, tx = rx + int(f[0]), tx + int(f[8])
    return rx, tx


def human(bps):
    for unit in ("B", "K", "M", "G"):
        if bps < 1000:
            return f"{bps:.0f}{unit}" if unit == "B" or bps >= 10 else f"{bps:.1f}{unit}"
        bps /= 1000
    return f"{bps:.0f}T"


def density(bps):  # log scale: ~1 KB/s barely drizzles, ~10 MB/s pours
    return max(0.0, min(1.0, (math.log10(bps + 1) - 3) / 4))


def braille(grid):
    rows = []
    for r in range(0, DOTROWS, 4):
        row = ""
        for c in range(0, COLS, 2):
            bits = sum(b for dx, dy, b in BRAILLE if grid[r + dy][c + dx])
            row += chr(0x2800 + bits)
        rows.append(row)
    return "<span line_height='0.75'>" + "\n".join(rows) + "</span>"


def ifaces_tip():
    try:
        out = subprocess.run(["ip", "-br", "-4", "addr"], capture_output=True, text=True).stdout
        return "\n".join(l.split()[0] + "  " + (l.split()[2] if len(l.split()) > 2 else "-")
                         for l in out.splitlines() if not l.startswith(("lo", "virbr")))
    except Exception:
        return socket.gethostname()


def net():
    down, up = set(), set()   # dot positions (row, col); left half = download, right half = upload
    rx0, tx0 = net_bytes()
    tip, tip_at = ifaces_tip(), time.time()
    while True:
        time.sleep(1 / FPS)
        rx, tx = net_bytes()
        rbps, tbps = (rx - rx0) * FPS, (tx - tx0) * FPS
        rx0, tx0 = rx, tx
        half = COLS // 2
        down = {(r + 1, c) for r, c in down if r + 1 < DOTROWS}      # rain falls
        up = {(r - 1, c) for r, c in up if r - 1 >= 0}               # and rises
        for c in range(half):
            if random.random() < density(rbps):
                down.add((0, c))
            if random.random() < density(tbps):
                up.add((DOTROWS - 1, c + half))
        grid = [[(r, c) in down or (r, c) in up for c in range(COLS)] for r in range(DOTROWS)]
        if time.time() - tip_at > 30:
            tip, tip_at = ifaces_tip(), time.time()
        cls = "busy" if max(rbps, tbps) > 1_000_000 else "idle" if max(rbps, tbps) < 1000 else "active"
        emit(braille(grid), f"↓ {human(rbps)}/s  ↑ {human(tbps)}/s\n{tip}", cls)


{"cpu": cpu, "net": net}[sys.argv[1]]()
