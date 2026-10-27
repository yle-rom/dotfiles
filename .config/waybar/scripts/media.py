#!/usr/bin/env python3
"""Media controls + now playing for the bottom bar (playerctl).
  media.py ctl prev|play|next  button glyph, event-driven (playerctl --follow status)
  media.py track               "artist — title  ████░░░░", polled every second
  media.py pet                 the pet, walking in whatever width the title leaves, up to just before cava (AVAIL)
"""
import html, json, random, subprocess, sys, time, unicodedata

import toys  # pet sprites, Typing, kbd_irqs, cpu_temp, braille bits

CELLS = 24        # progress bar
MAXLEN = 48       # title, in cells
AVAIL = 926       # px from the title start to 12px before cava, minus the pet padding (measured: title x=116, cava x=1066)
                  # depends on button widths and cava width/padding: re-measure if those change
FPS = 6


def out(text, cls, tooltip=""):
    print(json.dumps({"text": text, "class": cls, "tooltip": tooltip}), flush=True)


def ctl(which):
    glyphs = {"prev": ("\U000f04ae",) * 2, "next": ("\U000f04ad",) * 2, "play": ("\U000f03e4", "\U000f040a")}  # 󰒮 󰒭 󰏤/󰐊
    proc = subprocess.Popen(["playerctl", "--follow", "status"], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        status = line.strip()
        if status not in ("Playing", "Paused"):
            out("", "none")
            continue
        out(glyphs[which][status == "Paused"], status.lower())


def cells(s):  # display width: CJK is two cells wide
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def clip(s, n):
    while cells(s) > n:
        s = s[:-2] + "…"
    return s


def now_playing():
    fmt = "{{status}}\t{{artist}}\t{{title}}\t{{position}}\t{{mpris:length}}"
    r = subprocess.run(["playerctl", "metadata", "--format", fmt], capture_output=True, text=True)
    parts = r.stdout.rstrip("\n").split("\t")
    if r.returncode or len(parts) < 5 or parts[0] not in ("Playing", "Paused"):
        return None
    status, artist, title, pos, length = parts
    name = clip(f"{artist} — {title}" if artist else title, MAXLEN)
    pos, length = int(pos or 0), int(length or 0)
    filled = round(CELLS * pos / length) if length else 0
    return status, name, "█" * filled + "░" * (CELLS - filled)


SW = 8                                                   # the original front-facing pet (toys.PET), 8x6 on rows 2-7
TOP = 2


class Pet:  # the right-bar pet turned sideways: walks left/right on an 8-dot-tall strip (2 braille rows)
    def __init__(self):
        self.x, self.vx, self.pause, self.tick = 0, 1, 0, 0
        self.last_key, self.keys0 = time.time(), toys.kbd_irqs()
        self.typing = toys.Typing()

    def rows(self, width):  # width in dots; returns the 2 braille rows
        self.tick += 1
        k = toys.kbd_irqs()
        if k != self.keys0:
            self.last_key, self.keys0 = time.time(), k
        asleep = time.localtime().tm_hour < 7 or time.time() - self.last_key > 120
        hot = toys.cpu_temp() >= 80
        speed = 1 + (self.typing.update() >= 60) + (self.typing.ratio >= 100)
        excited = speed > 1
        span = width - SW
        self.x = max(0, min(span, self.x))                            # track shrinks when a longer title comes in
        if asleep:
            sprite = toys.PET["sleep"]
        else:
            if excited:
                self.pause = 0
            if self.pause:
                self.pause -= 1
            elif random.random() < 0.05 and not excited:
                self.pause = random.randint(4, 16)
            else:
                for _ in range(speed):
                    self.x += self.vx
                    if self.x <= 0 or self.x >= span or (random.random() < 0.04 and not excited):
                        self.vx *= -1
                        self.x = max(0, min(span, self.x))
            sprite = (toys.PET["blink"] if self.tick % 23 == 0
                      else toys.PET["step"] if (not self.pause and self.tick % 2) else toys.PET["open"])
        right = self.vx > 0
        g = [[False] * width for _ in range(8)]
        for dy, row in enumerate(sprite):
            for dx, ch in enumerate(row):
                if ch == "#":
                    g[TOP + dy][self.x + dx] = True
        zx = self.x + SW + 1 if right else self.x - 4                 # one small z beside the head, blinking
        if asleep and 0 <= zx and zx + 3 <= width:
            if self.tick // 4 % 2:
                for dy, row in enumerate(["###", ".#.", "###"]):
                    for dx, ch in enumerate(row):
                        if ch == "#":
                            g[dy][zx + dx] = True
        if hot and not asleep and self.tick % 4 < 2:
            g[1][self.x + 7] = True                                   # sweat drop, top right like the right-bar pet
        return ["".join(chr(0x2800 + sum(b for (bx, by), b in toys.BIT.items() if g[r + by][c + bx]))
                        for c in range(0, width, 2)) for r in (0, 4)]


def track():  # title + progress bar; polled every second
    while True:
        info = now_playing()
        if info:
            status, name, bar = info
            out(f"{html.escape(name)}  <span alpha='75%'>{bar}</span>", status.lower())
        else:
            out("", "none")
        time.sleep(1)


def pet():  # its own module right after the track: same playerctl read, so its width = whatever the title leaves
    p, info, polled = Pet(), None, 0
    while True:
        if time.time() - polled >= 1:
            info, polled = now_playing(), time.time()
        used = cells(f"{info[1]}  {info[2]}") if info else 0
        r1, r2 = p.rows((AVAIL - used * 6) // 7 * 2)             # title cells are 6px; the pet is JetBrains braille, 7px a char
        out(f"<span line_height='1.0'>{r1}\n{r2}</span>", "pet")
        time.sleep(1 / FPS)


if __name__ == "__main__":
    {"ctl": lambda: ctl(sys.argv[2]), "track": track, "pet": pet}[sys.argv[1]]()
