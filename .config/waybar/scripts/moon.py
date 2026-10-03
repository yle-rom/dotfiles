#!/usr/bin/env python3
"""Moon phase, computed locally (no network). Persona 3-ish readout.
  moon.py image   -> draws a shaded moon PNG in the bar's color; prints "path\\ntooltip" (waybar image module)
  moon.py glyph   -> prints the matching Weather Icons glyph (28 phases)
  moon.py tooltip -> prints just the tooltip text"""
import math, os, re, sys
from datetime import datetime, timedelta, timezone

SYNODIC = 29.530588853                                    # days, new moon -> new moon
REF_NEW = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)  # a known new moon
COLORS = os.path.expanduser("~/.config/waybar/colors-active.css")
OUT = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "waybar-moon.png")


def phase(now=None):
    now = now or datetime.now(timezone.utc)
    age = ((now - REF_NEW).total_seconds() / 86400) % SYNODIC
    p = age / SYNODIC                                     # 0 new, .25 first quarter, .5 full, .75 last quarter
    illum = (1 - math.cos(2 * math.pi * p)) / 2
    return p, age, illum


def name(p):
    names = ["NEW MOON", "WAXING CRESCENT", "FIRST QUARTER", "WAXING GIBBOUS",
             "FULL MOON", "WANING GIBBOUS", "LAST QUARTER", "WANING CRESCENT"]
    return names[int((p * 8) + 0.5) % 8]


def eighths(illum):
    n = round(illum * 8)
    return {0: "NEW", 8: "FULL"}.get(n, f"{n}/8")        # Persona-style "x/8 moon"


def next_phase(age, target_age):
    days = (target_age - age) % SYNODIC
    return (datetime.now() + timedelta(days=days))


def tooltip():
    p, age, illum = phase()
    full = next_phase(age, SYNODIC / 2)
    new = next_phase(age, 0)
    return "\n".join([
        f"<b>{name(p)}</b> · {eighths(illum)}",
        f"lit {illum:.0%} · day {age:.1f} of {SYNODIC:.1f}",
        "",
        f"full moon  {full:%a %d %b}",
        f"new moon   {new:%a %d %b}",
    ])


def glyph():
    p, _, _ = phase()
    i = (int(p * 28 + 0.5) + 14) % 28                     # +14: this set fills the *shadow*; shift so lit = filled
    return chr(0xE3E3) if i == 0 else chr(0xE3C8 + i - 1)


def bar_color(name_, default):
    try:
        m = re.search(rf"@define-color\s+{name_}\s+(#[0-9a-fA-F]{{6}})", open(COLORS).read())
        h = (m.group(1) if m else default).lstrip("#")
    except OSError:
        h = default.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def image(size=96):
    import numpy as np
    from PIL import Image
    p, _, _ = phase()
    fg = np.array(bar_color("fg", "#5aaa53"), dtype=float)

    r = size / 2 - 2
    y, x = np.mgrid[0:size, 0:size].astype(float)
    nx, ny = (x - size / 2 + 0.5) / r, (y - size / 2 + 0.5) / r
    d2 = nx ** 2 + ny ** 2
    inside = d2 <= 1
    nz = np.sqrt(np.clip(1 - d2, 0, 1))

    # sun direction: behind the moon at new (z=-1), from the right at first quarter, in front at full
    th = 2 * math.pi * p
    light = nx * math.sin(th) + nz * -math.cos(th)
    lit = np.clip(light * 3 + 0.15, 0, 1)                 # soft terminator

    # surface: a few maria (dark seas) + small craters + grain, fixed so the moon always looks the same
    albedo = np.ones_like(nx)
    for cx, cy, s, k in [(-.25, -.35, .28, .42), (.15, -.30, .22, .36), (.35, .05, .20, .32),
                         (-.35, .15, .25, .38), (-.05, .35, .18, .30), (.05, .0, .12, .22)]:
        albedo -= k * np.exp(-(((nx - cx) ** 2 + (ny - cy) ** 2) / (2 * s * s)))
    rng = np.random.default_rng(3)
    for _ in range(8):
        cx, cy, s = rng.uniform(-.8, .8), rng.uniform(-.8, .8), rng.uniform(.03, .08)
        dd = np.sqrt((nx - cx) ** 2 + (ny - cy) ** 2)
        albedo -= .10 * np.exp(-(dd ** 2) / (2 * s * s))                 # small crater
    albedo += rng.normal(0, .04, albedo.shape)
    albedo = np.clip(albedo, .35, 1.05)

    limb = 0.55 + 0.45 * nz                              # darker toward the edge
    bright = lit * albedo * limb
    earthshine = 0.10 * albedo                           # faint dark side, so the full disc reads (Persona look)
    level = np.maximum(bright, earthshine)

    rgb = (fg[None, None, :] * (0.35 + 0.95 * level[..., None])).clip(0, 255)
    alpha = np.where(inside, 255 * np.clip(0.25 + level * 1.2, 0, 1), 0)
    edge = np.clip((1 - np.sqrt(d2)) * r, 0, 1)          # anti-aliased rim
    alpha = alpha * edge
    img = np.dstack([rgb, alpha]).astype(np.uint8)
    Image.fromarray(img, "RGBA").save(OUT)
    return OUT


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "image"
    if mode == "image":
        print(image())
        print(tooltip().replace("\n", "&#10;"))          # waybar reads one tooltip line; &#10; = markup newline
    elif mode == "glyph":
        print(glyph())
    else:
        print(tooltip())
