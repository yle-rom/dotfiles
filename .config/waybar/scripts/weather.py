#!/usr/bin/env python3
"""Weather for waybar via wttr.in (no API key). Icon + temp, details in the tooltip.
Location: auto from IP. To pin it, set LOCATION below (e.g. "Ioannina").
  weather.py            -> weather icon + temp
  weather.py --moon     -> moon phase glyph + temp; tooltip = moon + weather
  weather.py --no-icon  -> temp only (e.g. with the moon image module above it)"""
import json, os, sys, time, urllib.request
from datetime import datetime

LOCATION = ""
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "waybar-weather.json")

# Solid icon set (Material Design), to match the solid heart / vinyl
SUN, MOON, CLOUD = "\U000F05A8", "\U000F0F65", "\U000F015F"
DROP, BOLT, FLAKE = "\U000F058C", "\U000F0241", "\U000F0717"
DAY = {113: SUN, 116: CLOUD}                 # clear, partly cloudy
NIGHT = {113: MOON, 116: CLOUD}
CLOUDY = CLOUD
ICONS = [
    ({119, 122}, CLOUD),
    ({143, 248, 260}, CLOUD),                                                # fog (no solid fog icon)
    ({200, 386, 389, 392, 395}, BOLT),                                       # thunderstorm
    ({176, 263, 266, 293, 296, 299, 302, 305, 308, 353, 356, 359}, DROP),    # rain, showers
    ({182, 185, 281, 284, 311, 314, 317, 320, 350, 362, 365, 374, 377}, DROP),  # sleet
    ({179, 227, 230, 323, 326, 329, 332, 335, 338, 368, 371}, FLAKE),        # snow
]


def fetch():
    req = urllib.request.Request(f"https://wttr.in/{LOCATION}?format=j1", headers={"User-Agent": "curl"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.load(r)
    with open(CACHE, "w") as f:
        json.dump(data, f)
    return data, False


def icon_for(code, night):
    if code in DAY:
        return (NIGHT if night else DAY)[code]
    return next((i for codes, i in ICONS if code in codes), CLOUDY)


def is_night(day):
    astro = day["astronomy"][0]
    now = datetime.now().time()
    rise = datetime.strptime(astro["sunrise"], "%I:%M %p").time()
    sset = datetime.strptime(astro["sunset"], "%I:%M %p").time()
    return not (rise <= now < sset)


try:
    data, stale = fetch()
except Exception:
    try:
        data, stale = json.load(open(CACHE)), True
    except Exception:
        print(json.dumps({"text": CLOUDY + "\n--", "tooltip": "weather unavailable", "class": "error"}))
        raise SystemExit

cur = data["current_condition"][0]
today = data["weather"][0]
tmrw = data["weather"][1]
area = data["nearest_area"][0]["areaName"][0]["value"]
icon = icon_for(int(cur["weatherCode"]), is_night(today))

hours = []
for h in today["hourly"]:
    t = int(h["time"]) // 100
    if t > datetime.now().hour:
        hours.append(f"{t:02d}:00  {icon_for(int(h['weatherCode']), False)}  {h['tempC']:>3}°  {h['chanceofrain']:>3}% rain")
tooltip = "\n".join([
    f"<b>{area}</b> · {cur['weatherDesc'][0]['value']}",
    f"{cur['temp_C']}°C, feels {cur['FeelsLikeC']}°C",
    f"today {today['mintempC']}° / {today['maxtempC']}°",
    f"humidity {cur['humidity']}% · wind {cur['windspeedKmph']} km/h",
    *([""] + hours[:4] if hours else []),
    "",
    f"tomorrow {tmrw['mintempC']}° / {tmrw['maxtempC']}° · {tmrw['hourly'][4]['weatherDesc'][0]['value'].strip()}",
    *(["", "<i>offline: showing last update</i>"] if stale else []),
])
mode = sys.argv[1] if len(sys.argv) > 1 else ""
if mode == "--moon":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import moon
    icon_markup = f"<span font_family='JetBrainsMono NFP' size='14pt'>{moon.glyph()}\u200a</span>\n"
    tooltip = moon.tooltip() + "\n\n" + tooltip
elif mode == "--no-icon":
    icon_markup = ""
else:
    icon_markup = f"<span font_family='JetBrainsMono NFM' size='13.5pt'>{icon}</span>\n"
print(json.dumps({
    "text": f"{icon_markup}{cur['temp_C']}°",
    "tooltip": tooltip,
    "class": "stale" if stale else "ok",
}))
