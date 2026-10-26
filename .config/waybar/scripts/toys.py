#!/usr/bin/env python3
"""Right-bar toys. Usage: toys.py sync|rain|pet [pet track height in dots, default 28]
  sync  Eva-style "sync ratio" = your typing speed in wpm (100 wpm = 100%), from the keyboard's interrupt count
  rain  half-width katakana falling Matrix-style
  pet   a braille creature: wanders, blinks, sleeps at night or after 2 min without typing, sweats at >= 80°C,
        bounces faster the higher the sync ratio (2x from 60%, 3x from 100%)"""
import collections, glob, json, random, sys, time

MODE = sys.argv[1]
BIT = {(0, 0): 0x01, (0, 1): 0x02, (0, 2): 0x04, (1, 0): 0x08, (1, 1): 0x10, (1, 2): 0x20, (0, 3): 0x40, (1, 3): 0x80}
W = 8                                          # dot columns (4 braille cells = the bar's width)


def emit(text, cls="", tip=""):
    print(json.dumps({"text": text, "class": cls, "tooltip": tip or MODE}), flush=True)


def braille(grid):  # grid[y][x] bools, height multiple of 4 -> text rows
    return ["".join(chr(0x2800 + sum(b for (dx, dy), b in BIT.items() if grid[r + dy][c + dx]))
                    for c in range(0, W, 2)) for r in range(0, len(grid), 4)]


def tight(rows):
    return "<span line_height='0.75'>" + "\n".join(rows) + "</span>"


# ---------- sync ratio: Eva pilot readout driven by typing speed ----------
def kbd_irqs():
    for line in open("/proc/interrupts"):
        if line.split(":")[0].strip() == "1" and "i8042" in line:
            return sum(int(v) for v in line.split()[1:] if v.isdigit())
    return 0


# ~2.1 interrupts per typed character (press + release): measured 574 IRQs for a 274-char test typed in 39 s
IRQ_PER_KEY = 2.1
WINDOW = 3                                     # seconds of typing averaged; drops to 0 this long after you stop


class Typing:  # typing speed over the last WINDOW seconds, eased (sync and pet each keep one)
    def __init__(self):
        self.hist = collections.deque()        # (time, irq count)
        self.ratio = 0.0

    def update(self):
        t, k = time.time(), kbd_irqs()
        self.hist.append((t, k))
        while self.hist[0][0] < t - WINDOW:
            self.hist.popleft()
        keys = (k - self.hist[0][1]) / IRQ_PER_KEY
        # divide by how long you've been typing within the window (min 1s), not the whole window:
        # reads your real speed after ~1s instead of ramping up over WINDOW seconds
        started = next((ht for (ht, hk), (_, nk) in zip(self.hist, list(self.hist)[1:]) if nk != hk), t)
        span = max(1.0, min(WINDOW, t - started))
        self.wpm = keys / 5 / span * 60
        target = min(999.0, self.wpm)          # sync ratio = wpm, 1:1
        self.ratio += (target - self.ratio) * (0.5 if target > self.ratio else 0.6)
        return self.ratio


def sync():
    typing = Typing()
    last = None
    while True:
        ratio = typing.update()
        wpm = typing.wpm
        shown = max(0.0, ratio + (random.uniform(-0.3, 0.3) if ratio > 1 else 0))
        cls = "berserk" if shown >= 130 else ""
        whole, dec = int(shown), int(shown * 10) % 10
        # whole number over ".d%": at most 3 digits per line, so the bar never widens
        text = (f"<span size='7.5pt'>SYNC</span>\n"   # one step bigger than before (6pt) so it reads bolder
                f"{whole}\n<span size='7pt'>.{dec}%</span>")   # number at 12px like the battery % and temperature, decimal smaller
        out = (text, cls, f"sync ratio {shown:.1f}% · {wpm:.0f} wpm")
        if out != last:                        # only on change: re-sending every frame keeps the bar's tooltips from showing
            emit(*out)
            last = out
        time.sleep(1 / 4)


# ---------- katakana rain: half-width kana falling, bright head, fading trail ----------
def rain():
    KANA = [chr(c) for c in range(0xFF66, 0xFF9E)]
    COLS, ROWS = 4, 14
    heads = [random.randint(-ROWS, ROWS) for _ in range(COLS)]
    lens = [random.randint(4, 9) for _ in range(COLS)]
    speed = [random.choice((1, 1, 2)) for _ in range(COLS)]
    chars = [[random.choice(KANA) for _ in range(COLS)] for _ in range(ROWS)]
    tick = 0
    while True:
        tick += 1
        for c in range(COLS):
            if tick % speed[c] == 0:
                heads[c] += 1
            if heads[c] - lens[c] > ROWS:
                heads[c], lens[c], speed[c] = random.randint(-8, -1), random.randint(4, 9), random.choice((1, 1, 2))
        for _ in range(3):                                           # random glyphs mutate
            chars[random.randrange(ROWS)][random.randrange(COLS)] = random.choice(KANA)
        rows = []
        for r in range(ROWS):
            cells = []
            for c in range(COLS):
                d = heads[c] - r
                if d == 0:
                    cells.append(f"<span foreground='white'>{chars[r][c]}</span>")
                elif 0 < d < lens[c]:
                    cells.append(f"<span alpha='{max(15, 100 - d * 90 // lens[c])}%'>{chars[r][c]}</span>")
                else:
                    cells.append(" ")
            rows.append("".join(cells))
        emit("<span line_height='0.85'>" + "\n".join(rows) + "</span>")
        time.sleep(1 / 8)


# ---------- braille pet: wanders the strip, blinks, sleeps at night or when idle, sweats when the CPU is hot ----------
PET = {
    "open":  ["..#..#..", ".######.", "##.##.##", "########", ".######.", ".#....#."],
    "blink": ["..#..#..", ".######.", "########", "########", ".######.", ".#....#."],
    "step":  ["..#..#..", ".######.", "##.##.##", "########", ".######.", "#......#"],
    "sleep": ["........", "..#..#..", ".######.", "##.##.##", "########", "########"],
}
PET["sleep"][3] = "#..##..#"


def cpu_temp():
    for h in glob.glob("/sys/class/hwmon/hwmon*"):
        if open(f"{h}/name").read().strip() == "coretemp":
            return int(open(f"{h}/temp1_input").read()) // 1000
    return 0


def pet():
    H, y, vy, pause, tick = int(sys.argv[2]) if len(sys.argv) > 2 else 28, 10, 1, 0, 0
    last_key, keys0 = time.time(), kbd_irqs()
    typing = Typing()
    while True:
        tick += 1
        k = kbd_irqs()
        if k != keys0:
            last_key, keys0 = time.time(), k
        hour = time.localtime().tm_hour
        asleep = hour < 7 or time.time() - last_key > 120
        hot = cpu_temp() >= 80
        sync = typing.update()
        speed = 1 + (sync >= 60) + (sync >= 100)                     # 1 step/frame calm, 2 from 60%, 3 from 100% (you type ~84 wpm)
        excited = speed > 1
        if asleep:
            sprite = PET["sleep"]
        else:
            if excited:                                              # no dawdling while you type fast
                pause = 0
            if pause:
                pause -= 1
            elif random.random() < 0.05 and not excited:
                pause = random.randint(4, 16)
            else:
                for _ in range(speed):
                    y += vy
                    if y <= 0 or y >= H - 6 or (random.random() < 0.04 and not excited):
                        vy *= -1
                        y = max(0, min(H - 6, y))
            sprite = PET["blink"] if tick % 23 == 0 else PET["step"] if (not pause and tick % 2) else PET["open"]
        g = [[False] * W for _ in range(H)]
        for dy, row in enumerate(sprite):
            for x, ch in enumerate(row):
                if ch == "#":
                    g[y + dy][x] = True
        extra = ""
        if asleep:
            extra = ["z", " z", "  Z"][tick // 4 % 3]
        if hot and not asleep and tick % 4 < 2 and y > 0:
            g[y - 1][7] = True                                       # sweat drop
        text = f"<span size='7pt'>{extra or ' '}</span>\n" + tight(braille(g))
        mood = "asleep" if asleep else "hot" if hot else "excited" if excited else "awake"
        emit(text, mood, f"pet · {mood}")
        time.sleep(1 / 6)


{"sync": sync, "rain": rain, "pet": pet}[MODE]()
