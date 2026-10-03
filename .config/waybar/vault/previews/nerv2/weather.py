#!/usr/bin/env python3
"""Weather for waybar via wttr.in (no API key). Icon + temp, details in the tooltip.
Location: auto from IP. To pin it, set LOCATION below (e.g. "Ioannina")."""
import json, os, time, urllib.request
from datetime import datetime

LOCATION = ""
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "waybar-weather.json")

DAY = {113: "󰖙", 116: "󰖕"}
NIGHT = {113: "󰖔", 116: "󰼱"}
ICONS = [
    ({119, 122}, "󰖐"),
    ({143, 248, 260}, "󰖑"),
    ({200, 386, 389, 392, 395}, "󰖓"),
    ({299, 302, 305, 308, 356, 359}, "󰖖"),
    ({176, 263, 266, 293, 296, 353}, "󰖗"),
    ({182, 185, 281, 284, 311, 314, 317, 320, 350, 362, 365, 374, 377}, "󰙿"),
    ({179, 227, 230, 323, 326, 329, 332, 335, 338, 368, 371}, "󰖘"),
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
    return next((i for codes, i in ICONS if code in codes), "󰖐")


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
        print(json.dumps({"text": "󰖐\n--", "tooltip": "weather unavailable", "class": "error"}))
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
print(json.dumps({
    "text": f"<span font_family='JetBrainsMono NFM' size='15pt'>{icon}</span>\n{cur['temp_C']}°",
    "tooltip": tooltip,
    "class": "stale" if stale else "ok",
}))
